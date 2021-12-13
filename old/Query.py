import time
import threading
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient

# Load completed songs

records_loaded = []

with open('records.txt', mode='r', encoding='utf8') as f:
    records = f.readlines()
    records_loaded.extend([x.split('<>')[1].replace('\n', '') for x in records])


glee = []

with open('Glee.txt', mode='r', encoding='utf8') as f:
    records = f.readlines()
    glee.extend([x.split('<>')[1].replace('\n', '') for x in records])


theme_loaded = []

with open('theme_not_found.txt', mode='r', encoding='utf8') as f:
    records = f.readlines()
    theme_loaded.extend([x.split('<>')[1].replace('\n', '') for x in records])


songs_loaded = list(set(records_loaded + glee + theme_loaded))

client = MongoClient(host='localhost', port=27017)
db = client['Billboard']
collection = db['10yWeekly']
songs = collection.find()

songs_unloaded = []
for song in songs:
    if '+'.join([song['Performer'], song['Song']]) not in songs_loaded:
        songs_unloaded.append(song)

threads = 3
interval = len(songs_unloaded) // threads
data_dict = {key: [] for key in range(threads)}

count = 0
for song in songs_unloaded:
    try:
        data_dict[count // interval].append(song)
    except KeyError:
        data_dict[threads - 1].append(song)
    count += 1

headless = False


class SpiderThread(threading.Thread):
    def __init__(self, instance, threadID: int, data):
        threading.Thread.__init__(self)
        self.instance = instance
        self.threadID = threadID
        self.name = 'Thread_' + str(self.threadID)
        self.data = data

    def run(self):
        print("Thread starts：" + self.name)
        self.instance.fetch(self.threadID, self.data)
        print("Thread ends：" + self.name)


class Spider:
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless

    def get_driver(self):
        implicitly_wait_time = 10
        explicitly_wait_time = 10
        url = 'https://www.allmusic.com/search/songs/{}'
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"  # 懒加载模式，不等待页面加载完毕
        # json_resp = requests.get('http://localhost:8899/api/v1/proxies').json()
        # proxy = random.choice(json_resp['proxies'])
        # proxy_address = 'http://{}:{}'.format(proxy['ip'], proxy['port'])
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--proxy-server=%s' % proxy_address)
        proxy_address = '127.0.0.1:8081'
        chrome_options.add_argument('--proxy-server=%s' % proxy_address)
        if self.headless:
            chrome_options.add_argument('--headless')
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,  # 不加载图片
            }
        }
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options,
                                       desired_capabilities=capa)
        # driver = webdriver.Chrome('chromedriver', desired_capabilities=capa)
        self.driver.implicitly_wait(implicitly_wait_time)
        wait = WebDriverWait(self.driver, explicitly_wait_time)
        return self.driver, wait, url

    def fetch(self, threadID, data):
        driver, wait, url = self.get_driver()
        num = 0
        for song_dict in data:
            SongID = '+'.join([song_dict['Performer'], song_dict['Song']])
            song = urllib.parse.quote(
                song_dict['Song'].split(' (')[0].replace('F*ck', 'Fuck').replace('N****z', 'Niggaz').replace('S**t',
                                                                                                             'Shit')).replace(
                '/', '%2F')
            performer = urllib.parse.quote(
                song_dict['Performer'].split(' Featuring ')[0].split(' & ')[0].split(',')[0].split(' x ')[0].split(
                    ' X ')[0].split(' / ')[0].split(' Co-Starring ')[0].split(' With ')[0].split(' Duet With ')[
                    0].split(' vs ')[0].replace("'n'", " 'n' ").split(' (')[0].split(' Vs. ')[0])

            query = '+'.join([performer, song])
            print(threadID, ':', num, r'/', interval, query, '|', SongID)
            counts = 0

            response = driver.get(url.format(query))
            exit_flag_inner = 0
            while True:
                if exit_flag_inner == 1:
                    break
                counts += 1
                try:
                    content_xpath = '//*[@id="cmn_wrap"]/div[1]/div[2]'
                    content_condition = EC.presence_of_element_located((By.XPATH, content_xpath))
                    wait.until(content_condition)
                    top_result_xpath = '//*[@id="cmn_wrap"]/div[1]/div[2]/div/ul/li[1]/div[1]/a'
                    no_results_xpath = '//*[@id="cmn_wrap"]/div[1]/div[2]/div'
                    while True:
                        exit_flag_inner = 0
                        try:
                            click = driver.find_element_by_xpath(top_result_xpath).click()
                            theme_xpath = '//*[@id="cmn_wrap"]/div[1]/div[1]/section[2]/div[5]/div[2]'
                            theme_condition = EC.presence_of_element_located((By.XPATH, theme_xpath))
                            wait.until(theme_condition)
                            theme_element = driver.find_element_by_xpath(theme_xpath)
                            themes = theme_element.find_elements_by_tag_name('a')
                            theme_list_raw = [i.text for i in themes]
                            if theme_list_raw == ['Add Themes']:
                                with open('theme_not_found_{}.txt'.format(threadID), mode='a',
                                          encoding='utf8') as f:
                                    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                    f.write(current_time + '<>' + song_dict['Performer'] + '<>' + song_dict['Song'] + '\n')
                                exit_flag_inner = 1
                                break
                            else:
                                theme_list = []
                                for theme_name in theme_list_raw:
                                    if theme_name[-1] == ')':
                                        theme_name = theme_name.split(' (')[0]
                                    theme_list.append(theme_name)
                                with open('records_{}.txt'.format(threadID), mode='a', encoding='utf8') as f:
                                    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                    f.write(current_time + '<>' + song_dict['Performer'] + '<>' + song_dict['Song'] + '<>' + ','.join(theme_list) + '\n')
                                exit_flag_inner = 1
                                break

                        except NoSuchElementException:
                            try:
                                driver.find_element_by_xpath(no_results_xpath)
                                with open('search_not_found_{}.txt'.format(threadID), mode='a', encoding='utf8') as f:
                                    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                    f.write(current_time + '<>' + song_dict['Performer'] + '<>' + song_dict['Song'] + '\n')
                                exit_flag_inner = 1
                                break
                            except NoSuchElementException:
                                pass
                except TimeoutException:
                    if counts > 5:
                        driver.quit()
                        driver, wait, url = self.get_driver()
                        counts = 0
                    response = driver.get(url.format(query))
                except:
                    driver.quit()
                    with open('error_{}.txt'.format(threadID), mode='a', encoding='utf8') as f:
                        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        f.write(current_time + '<>' + song_dict['Performer'] + '<>' + song_dict['Song'] + '\n')
                    driver, wait, url = self.get_driver()
                    break
            num += 1
            print(threadID, ':', num, r'/', interval, 'succeeded')
        driver.quit()


t0 = time.time()
print('Program starts')

s = Spider(headless=headless)

thread_list = []
for i in range(threads):
    thread_list.append(SpiderThread(instance=s, threadID=i + 1, data=data_dict[i]))

t1 = time.time()
# print(t1 - t0)
print("Threads start")

for i in thread_list:
    i.start()
for i in thread_list:
    i.join()
t2 = time.time()

print(t2 - t1)
print("Threads end")
