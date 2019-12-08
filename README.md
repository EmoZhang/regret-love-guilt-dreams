# Billboard x AllMusic 数据报告

（我就随便瞎写一下，我姑妄说之您姑妄听之）

[TOC]

## 数据获取方法

1. 从 Billboard Hot 100 周榜获取所有上榜歌曲作为整体，其中 Billboard Hot 100 Year-end 榜单的歌曲作为“非常流行（Hits）”的样本，其余作为“比较流行（Non-Hits）”的样本，以此进行二元分类。
2. 在 AllMusic 网站搜索上述样本，获取其“主题（Theme）”标签。其中没有搜索结果的歌曲和没有被打上标签的歌曲从样本数据库中舍弃。
3. 最后通过 Spotify Web API 获取有效样本的 Audio Features（尚未进行）。

## 标签聚类

AllMusic 的 Theme 共有 182 个标签，冗余严重（x 

Bischoff, Kerstin & Claudiu, Sava & Paiu, Raluca & Nejdl, Wolfgang & Laurier, Cyril & Sordo, Mohamed. (2009). Music Mood and Theme Classification - a Hybrid Approach.. Proceedings of the 10th International Society for Music Information Retrieval Conference, ISMIR 2009. 657-662. （我被 APA 会议格式搞昏了，直接复制网站给的 citation 了将 AllMuisc 的 theme tags 按相似性做了聚类，并排除掉了一些收录歌曲过少的标签，原表如下：

| Cluster | Theme tags                                                   |
| ------- | ------------------------------------------------------------ |
| T1      | Party Time, Birthday Party, Celebration, Prom, Late Night, Guys Night Out, Girls Night Out, At the Beach, Drinking, Cool & Cocky, TGIF, Pool Party, Club, Summertime |
| T2      | Sex, Seduction, Slow Dance, Romantic Evening, In Love New Love, Wedding, Dinner Ambiance |
| T3      | Background Music, Exercise/Workout Music, Playful  The Sporting Life, Long Walk, The Great Outdoors, Picnic, Motivation, Empowering, Affirmation, The Creative Side, Victory, Day Driving, Road Trip, At the Office |
| T4      | D-I-V-O-R-C-E, Heartache, Feeling Blue, Breakup, Regret, Loss/Grief, Jealousy, Autumn, Rainy Day, Stay in Bed, Solitude, Reminiscing, Introspection, Reflection, Winter, Sunday Afternoon |

我在此基础上筛选并增补了一下暂且作为分类标准：

| Cluster | Theme tags                                                   |
| ------- | ------------------------------------------------------------ |
| Love    | Sex, Seduction, Romantic Evening, In Love, New Love, Wedding, Romance |
| Breakup | D-I-V-O-R-C-E, Breakup                                       |

大家可以根据后面的数据概览看看这个标准合不合适！还挺迷的。

## 数据清洗

根据 Billboard 网站的记录，2009 - 2018 年 Billboard Hot 100 周榜共上榜 4500 首歌曲。其中有 206 首 Glee（欢乐合唱团）的翻唱曲目，难以自动化搜索，故暂且舍弃。那么整体容量即 4294 首。其中年榜样本容量为 899 首（有重复上榜的情况，气死我了：）））。理论上其余的样本量即为 4295 - 899 = 3396 首。

吐槽：在获取数据的过程中，发现 Billboard 榜单的一个 bug：

2011 和 2016 year-end chart 分别缺一首歌，其中一首歌在周榜上也消失了，在维基百科查到后发现 AllMusic 也并没有给这两首歌打上标签。所以不妨就塞进数据库里作为无效样本了。。至于周榜里有没有缺的歌我就不管了嗯。

Anyway，清洗之后的样本容量如下：

| 整体 | Hits | Non-hits |
| ---- | ---- | -------- |
| 4295 | 901  | 3394     |




## 数据概览

打标签情况：

|          | 有标签 | 无标签 | 无搜索结果 | 汇总 |
| -------- | ------ | ------ | ---------- | ---- |
| Hits     | 143    | 752    | 6          | 901  |
| Non-hits | 349    | 2999   | 46         | 3394 |
| 整体     | 492    | 3751   | 52         | 4295 |

标签聚类情况：

|          | Love Songs | Breakup Songs | 其他 | 汇总 |
| -------- | ---------- | ------------- | ---- | ---- |
| Hits     | 54         | 22            | 67   | 143  |
| Non-hits | 107        | 40            | 202  | 349  |
| 整体     | 161        | 62            | 269  | 492  |

做了几个小图表：

### 整体

4295 首歌曲中共有 492 首有标签：

![whole_proportion](/Users/mac/PycharmProjects/LoveSongs/whole_proportion.png)

其中被打上标签的歌曲分布：

![whole_tag_distribution](/Users/mac/PycharmProjects/LoveSongs/whole_tag_distribution.png)

其中 Love Song 有 161 首，Breakup Song 有 62 首：

![whole_tag_clustering](/Users/mac/PycharmProjects/LoveSongs/whole_tag_clustering.png)

### Hits

901 首歌曲中共有 143 首有标签：

![hit_proportion](/Users/mac/PycharmProjects/LoveSongs/hit_proportion.png)

其中被打上标签的歌曲分布：

![hit_tag_distribution](/Users/mac/PycharmProjects/LoveSongs/hit_tag_distribution.png)

其中 Love Song 有 54 首，Breakup Song 有 22 首：

![hit_tag_clustering](/Users/mac/PycharmProjects/LoveSongs/hit_tag_clustering.png)

### Non-hits

3394 首歌曲中共有 349 首有标签：

![non_hit_proportion](/Users/mac/PycharmProjects/LoveSongs/non_hit_proportion.png)

其中被打上标签的歌曲分布：

![hit_tag_distribution](/Users/mac/PycharmProjects/LoveSongs/hit_tag_distribution.png)

其中 Love Song 有 54 首，Breakup Song 有 22 首：

![hit_tag_clustering](/Users/mac/PycharmProjects/LoveSongs/hit_tag_clustering.png)

## TODO

1. 确认目前的样本容量🉑️不🉑️
2. 确认目前的标签聚类标准🉑️不🉑️
3. 确认之后我再去搞 Spotify，嗯
