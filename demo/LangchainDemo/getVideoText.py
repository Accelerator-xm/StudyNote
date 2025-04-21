from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import random, time, datetime, re
from yt_dlp import YoutubeDL
from langchain.docstore.document import Document

COOKIE_FILE = "demo/LangchainDemo/www.youtube.com_cookies.txt"

def get_video_id(url: str) -> str | None:
    m = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11})", url)
    return m.group(1) if m else None

def load_youtube_video(url: str):
    video_id = get_video_id(url)
    if not video_id:
        raise ValueError("URL 无法解析到视频 ID")

    # ① 先取元数据
    ydl_opts = {
        "quiet": True,
        "cookiefile": COOKIE_FILE,
        "sleep_interval": 1,
        "max_sleep_interval": 3,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # ② 取字幕 —— 把 cookie 也传进去，并做退避
    for _ in range(4):                       # 最多 4 次指数退避
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=['zh-Hans', 'zh-Hant', 'en'],
                cookies=COOKIE_FILE          # ← 关键：同一份 cookie
            )
            break
        except TranscriptsDisabled:
            print(f"该视频无字幕: {url}")
            return []
        except Exception as e:               # 429、IP 被封等
            wait = random.uniform(2, 6)
            print(f"取字幕失败：{e}，{wait:.1f}s 后重试…")
            time.sleep(wait)
    else:
        raise RuntimeError("重试后仍无法获取字幕")

    full_text = "\n".join(seg['text'] for seg in transcript)

    publish_date = info.get('upload_date')   # '20240312'
    publish_date = (datetime.datetime.strptime(publish_date, '%Y%m%d')
                    .isoformat() if publish_date else 'Unknown')
    metadata = {
        "title": info.get('title', 'Unknown'),
        "channel": info.get('channel', 'Unknown'),
        "publish_date": publish_date,
        "video_id": video_id,
        "url": url,
    }
    return [Document(page_content=full_text, metadata=metadata)]
