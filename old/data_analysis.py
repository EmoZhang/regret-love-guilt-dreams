import matplotlib.pyplot as plt
import numpy as np

record_list = []
with open('records.txt', mode='r', encoding='utf8') as f:
    records = f.readlines()
    for i in records:
        __, Performer, Song, tag_str = i.replace('\n', '').split('<>')
        tags = tag_str.split(',')
        record_list.append([Performer, Song, tags])

with open('theme_not_found.txt', mode='r', encoding='utf8') as f:
    no_theme_count = len(f.readlines())

with open('search_not_found.txt', mode='r', encoding='utf8') as f:
    no_search_count = len(f.readlines())

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Got tags', "No tag", "No search result"
sizes_all = [len(record_list), no_theme_count, no_search_count]
size_all = sum(sizes_all)
explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()


def func(pct, allvals):
    absolute = int(round(pct / 100. * np.sum(allvals)))
    return "{:.1f}%\n({:d})".format(pct, absolute)


ax1.pie(sizes_all, explode=explode, labels=labels, autopct=lambda pct: func(pct, sizes_all),
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title(
    'AllMusic Theme Database Query Results\nof {} songs from Billboard Hot 100 during 2009-2018)'.format(size_all))
plt.savefig('pics/whole_proportion.png')

love_tags = ['Sex', 'Seduction', 'Romantic Evening', 'In Love', 'New Love', 'Wedding', 'Romance']
breakup_tags = ['D-I-V-O-R-C-E', 'Breakup']

tag_count = {}
for i in record_list:
    for tag in i[2]:
        try:
            tag_count[tag] += 1
        except KeyError:
            tag_count[tag] = 1
tag_list = []
for k, v in tag_count.items():
    if k in love_tags:
        c = (255 / 255, 182 / 255, 193 / 255)
    elif k in breakup_tags:
        c = (135 / 255, 206 / 255, 250 / 255)
    else:
        c = (240 / 255, 240 / 255, 240 / 255)
    tag_list.append([k, v, c])
tag_list = sorted(tag_list, key=lambda tag: tag[1], reverse=True)

# Fixing random state for reproducibility

plt.rcdefaults()
fig, ax = plt.subplots()
fig.set_size_inches(25, 25)

# Example data
tag_names = [tag[0] for tag in tag_list]
y_pos = np.arange(len(tag_names))
counts = [tag[1] for tag in tag_list]
# error = np.random.rand(len(tag_names))

# ax.barh(y_pos, performance, xerr=error, align='center')
rects = ax.barh(y_pos, counts, align='center', color=[tag[2] for tag in tag_list])
ax.set_yticks(y_pos)
ax.set_yticklabels(tag_names)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Counts')
ax.set_title('Tag Distribution\n({} songs out of {})'.format(len(record_list), size_all))


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for idx, rect in enumerate(rects):
        width = rect.get_width()
        ax.annotate(counts[idx],
                    xy=(width, rect.get_y() + rect.get_height()),
                    xytext=(10, 0),
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects)
plt.savefig('pics/whole_tag_distribution.png')

cluster = {
    'Love': [],
    "Breakup": []
}

for i in record_list:
    flag = False
    for tag in i[2]:
        # if tag in ['Sexy', 'Seduction', 'Romantic Evening', 'In Love', 'New Love', 'Wedding']:
        if tag in love_tags:
            cluster['Love'].append(i)
            break
        elif tag in breakup_tags:
            cluster['Breakup'].append(i)
            break
        else:
            pass

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Love', 'Breakup'
sizes = [len(cluster['Love']), len(cluster['Breakup'])]
explode = (0, 0,)

fig1, ax1 = plt.subplots()


def func(pct, allvals):
    absolute = int(round(pct / 100. * np.sum(allvals)))
    return "{:.1f}%\n({:d})".format(pct, absolute)


ax1.pie(sizes, explode=explode, labels=labels, autopct=lambda pct: func(pct, sizes),
        colors=[(255 / 255, 182 / 255, 193 / 255), (135 / 255, 206 / 255, 250 / 255)], shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title(
    'Tag Clustering\n({} songs out of {})'.format(sum(sizes), len(record_list)))
plt.savefig('pics/whole_tag_clustering.png')
