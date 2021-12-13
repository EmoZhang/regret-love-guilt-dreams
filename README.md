# Spotify 数据报告

- [Spotify 数据报告](#spotify-数据报告)
  * [数据获取策略](#数据获取策略)
  * [标签聚类](#标签聚类)
  * [数据清洗](#数据清洗)
  * [数据概览](#数据概览)
  * [TODO](#todo)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## 数据获取策略

1. 从 Billboard Hot 100 周榜获取所有上榜歌曲作为样本总体，其中 Billboard Hot 100 Year-end 榜单的歌曲作为“非常流行（Hits）”的样本，其余作为“比较流行（Non-Hits）”的样本，以此进行二元分类。
2. 在 AllMusic 网站搜索上述样本，获取其“主题（Theme）”标签。其中没有搜索结果的歌曲和没有被打上标签的歌曲从样本数据库中舍弃。
3. 最后通过 Spotify Web API 获取有效样本的 Audio Features。

## 标签聚类


| Clusters | Theme tags                                                   |
| ------- | ------------------------------------------------------------ |
| Love    | Sex, Seduction, Romantic Evening, In Love, New Love, Wedding, Romance |
| Breakup | D-I-V-O-R-C-E, Breakup                                       |

## 数据清洗

Spotify 没有版权的歌共有 3 首。


## 数据概览

|          | Love Songs | Breakup Songs | 汇总 |
| -------- | ------ | ------ | ---- |
| Hits     |     |     |   |
| Non-hits |     |    |  |
| 样本总体  |     |    |  |

Spotify Web API 提供的（有用的） Audio Features 字段包括以下 13 个：

| KEY              | VALUE TYPE | VALUE DESCRIPTION                                            |
| :--------------- | :--------- | :----------------------------------------------------------- |
| acousticness     | float      | A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic. |
| danceability     | float      | Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable. |
| duration_ms      | int        | The duration of the track in milliseconds.                   |
| energy           | float      | Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy. |
| instrumentalness | float      | Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0. |
| key              | int        | The key the track is in. Integers map to pitches using standard [Pitch Class notation](https://en.wikipedia.org/wiki/Pitch_class). E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. |
| liveness         | float      | Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live. |
| loudness         | float      | The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db. |
| mode             | int        | Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0. |
| speechiness      | float      | Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks. |
| tempo            | float      | The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. |
| time_signature   | int        | An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure). |
| valence          | float      | A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry). |

## TODO

1. 清洗数据
2. 机器学习（一共两百多样本，love一百多，breakup不到一百，再取1/4做测试集