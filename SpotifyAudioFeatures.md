# Spotify Audio Features 名词解释
- [Spotify Audio Features 名词解释](#spotify-audio-features-名词解释)
  * [acousticness](#acousticness)
  * [danceability](#danceability)
  * [duration_ms](#duration-ms)
  * [energy](#energy)
  * [instrumentalness](#instrumentalness)
  * [key](#key)
  * [liveness](#liveness)
  * [loudness](#loudness)
  * [mode](#mode)
  * [speechiness](#speechiness)
  * [tempo](#tempo)
  * [time_signature](#time-signature)
  * [valence](#valence)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


Spotify Web API 提供的（有用的） Audio Features 字段包括以下 13 个：

## acousticness

“原声程度”。 浮点数（即小数）。

<blockquote>A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.</blockquote>


首先解释一下“acoustic”这个词，指的是“原声的”或者“自然声的”，也就是所有你能想到的不插电的“传统”乐器，比如木吉他、钢琴、弦乐、铜管、木管、鼓等等。与之对应的则是插电的乐器，比如电吉他、合成器以及任何你在电音里听到的奇怪声音。

Acousticness 则是一个从 0.0 到 1.0 的信度，描述的是一首歌多大程度是 acoustic 的。

1.0 代表这首歌很大程度上是一首原声歌曲（比如理查德克莱德曼浪漫钢琴曲《梦中的婚礼》或者《南山南》之类的：））。

## danceability

“可跳舞性”。 浮点数。

<blockquote>Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.</blockquote>


顾名思义指的就是一首歌有多适合跳舞。

这个指标基于各种音乐因素，比如节拍、节奏有多稳定、拍子有多猛，以及整体上是不是很有规律（跳舞嘛当然整首歌动词打次最适合）。

0.0 表示宁可憋蹦了，1.0 表示好嗨哦。

## duration_ms

时长。整数。

<blockquote>The duration of the track in milliseconds.</blockquote>


没啥可说的。单位毫秒。

## energy

能量。浮点数。

<blockquote>Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.</blockquote>


这个测度取值从 0.0 到 1.0，代表的是一首歌在感知层面上有多强烈/有多猛。

一般来说，能量高的歌快、响、吵。比如死亡金属就很高能，而巴赫的钢琴小曲能量就很低。

这个参数的影响因素包括一首歌的动态范围（最静和最响的差距）、感知的响度、音色/音质、声音起始点的什么什么比率（就所有声音都有一个起始点，有的比较“硬”，比如钢琴、吉他，有的比较“软”，比如提琴，我估计就是这个意思）和整体的熵（混乱程度/无序程度）。（听起来有点玄学不过你从感知上应该能 get 到）

## instrumentalness

“纯音乐程度”。浮点数

<blockquote>Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.</blockquote>


还是先解释一下“instrumental”，也就是所谓“纯音乐”或者类似“伴奏带”的形容词。

这个参数预测的是一首歌是否**不**含人声。“哦哦哦”和“啊啊啊”这种声音在这个 context 下面被认为也是“纯音乐”。而说唱或者说话（比如念了两句诗）当然是“人声”。

该参数越接近 1.0，这首就越可能不含人声。大于 0.5 的值倾向于认为这首歌是纯音乐，越接近 1.0 信度越高。（我们的数据里最高才一点点而已，也就是说所有歌都有人声，所以这个指标没有什么p用）

## key

调。整数。

<blockquote>The key the track is in. Integers map to pitches using standard [Pitch Class notation](https://en.wikipedia.org/wiki/Pitch_class). E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on.</blockquote>


这个歌是什么调，也就是CDEFGAB啥的。

这个参数实际上是一个分类变量，给到我们的已经做了标签编码，也就是按照这个东西 [Pitch Class notation](https://en.wikipedia.org/wiki/Pitch_class) 把每个调映射到了一个整数：0 = C调，1 = C♯/D♭调，以此类推。

## liveness

“现场程度”。浮点数。

<blockquote>Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.</blockquote>


还是解释一下“live”，也就是“现场版”的意思。

这个参数检测的是录音里观众是否在场。

越高的值代表这首歌越可能是现场录音。如果超过 0.8 说明这首歌非常有可能就是现场录音。

## loudness

响度。浮点数。

<blockquote>The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.</blockquote>


一首歌总体的响度，单位分贝（dB）。这个指标是整首歌的平均响度，可以用来比较不同歌曲的相对响度。

Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). 。。。我不会翻译这句话。但是意思就是响度是与声强相对应的声音大小的知觉量。啥意思呢，就是说这东西的度量依靠的是听觉而不是单纯的声强，耳朵觉得它有多响才是有多响。（其实知道了对于我们的任务也没啥用。。）

## mode

调性。整数。

<blockquote>Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.</blockquote>


调性嘛指的就是大调/小调，也就是这首歌是基于什么样的音阶（别管了）。

这也是一个做好了标签编码的分类变量，1 代表大调，0 代表小调。

## speechiness

“是讲话的程度”（我实在翻译不出）。浮点数。

<blockquote>Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.</blockquote>


这个参数检测的是一首歌里是否有“讲话”存在。

录音里单独讲话的部分越多（比如脱口秀、有声书、念诗），值越接近 1.0. 超过 0.66 表示这首“歌”可能在全程讲话；0.33 到 0.66 代表这首歌既有音乐又有讲话，可能是一部分一部分分开的，也可能是叠加在一起的，这种情形包括了说唱；小于 0.33 表示这首歌只包含音乐或者其他什么不像讲话的声音。

## tempo

（乐曲的）速度。浮点数。

<blockquote>The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.</blockquote>


一首歌 BPM 的总体估计值。BPM 就是 beats per minute （每分钟的拍数）的缩写，比如每分钟 60 拍就是挺慢挺悠扬的一首歌，120 拍就蛮快蛮活泼的。有一种金属乐风格叫 doom metal，极其缓慢且压抑，有的甚至慢到 30bpm 以下；有一种硬核电子乐（没错这个风格的名字本来就叫 hardcore）叫 speedcore，极其快，一般都要在 300bpm 以上，超过 1000bpm 之后就有了新名字叫 extratone，我实在不知道这玩意咋蹦。

（这段别看了，没有p用）作为一个音乐术语，tempo 指的是一段音乐的速度或者说“pace”（能 get 吗？？不能也没关系。因为古典音乐原初的谱子上不会写什么每分钟多少拍，只会写“柔板”“行板”“急板”这种鬼东西，全靠自己体悟），从平均每拍多长得出。

## time_signature

拍号。整数。

<blockquote>An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure).</blockquote>


拍号是一种用来具体说明每小节有多少拍的标记法则。

具体解释一下。我们经常看到的拍号是有3/4、4/4这种东西，这玩意看似是个分数，实际上和分数没啥关系。分母指的是以哪个时值的音符为一拍，分子指的是每小节有几拍。所以3/4拍读作“四三拍”，意思是“以四分音符为一拍，每小节三拍”。

没学过基础乐理的朋友读到这里可能有点晕，啥东西是一拍怎么还需要定义呢。其实解释起来也不难，不过在我们的研究里不必掌握那么详细！感兴趣可以查一查或者问我！我们只需要考虑分子就可以了！也就是“每小节有几拍”。我们平时最常听到的动词打次就是四拍子，为什么，你数啊，动、词、打、次，正好四拍对不对。最典型的三拍子音乐就是圆舞曲或者说华尔兹，流行歌曲比如E神的《浮夸》、汪峰的《春天里》、王菲的《笑忘书》（其实到底是三拍子还是六拍子是可以讨论的也是无所谓的，这里就说是三拍子了嗯）。在我们的数据样本里，Spotify 给出的值有1、3、4、5，这其实也是个分类变量。

但是，我是不知道为什么会有一拍子这种神奇节拍。我斗胆猜测它把识别不出来的全都丢这里了？？？咱也不敢问。

## valence

（实在不晓得怎么翻译）。浮点数

<blockquote>A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).</blockquote>

这个取值从 0.0 到 1.0 的参数描述的是一首歌所传达的“积极性”。

值越高的歌听起来越“积极”（比如充满了快活的空气），而值越低的歌听起来越“消极”（比如伤心、抑郁、愤怒）。