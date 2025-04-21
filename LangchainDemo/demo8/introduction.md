# langchain检索YouTube视频字幕

- demo介绍
    - getVideoText.py: yt_dlp+youtube-transcript-api爬取视频字幕
    - youtube_vectorDB.py: 爬取视频字幕构建向量数据库，持久化存储
    - retrieval_vectorDB.py：加载向量数据库，智能化检索
    - chroma_data_dir: 向量数据库存储文件夹
