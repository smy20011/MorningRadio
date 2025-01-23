from feedgen.feed import FeedGenerator
from pathlib import Path
import glob
import os
import datetime
import jinja2

PODCAST_TITLE = "Morning Routine"
PODCAST_DESCRIPTION = "Programmatically Generated Podcast"
ASSETS_DIR = "assets"  # Directory where your MP3 files are stored


def homepage():
    episodes = get_episodes()
    env = jinja2.Environment(loader = jinja2.FileSystemLoader("templates"))
    template = env.get_template("index.html")
    return template.render(episodes=episodes, podcast_title=PODCAST_TITLE, podcast_description=PODCAST_DESCRIPTION)

def rss_feed():
    episodes = get_episodes()
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.title(PODCAST_TITLE)
    fg.link(href=f"/")
    fg.description(PODCAST_TITLE)

    for episode in episodes:
        fe = fg.add_entry()
        url = f"{episode['filename']}"
        fe.id(url)
        fe.title(f"{PODCAST_TITLE} {episode['creation_time'].strftime('%Y-%m-%d')}")
        fe.enclosure(url, 0,  'audio/mpeg')
        fe.published(episode['creation_time'])
        fe.guid(url)

    return fg.rss_str(pretty=True)

def get_episodes():
    episodes = []
    for file in glob.glob(f"{ASSETS_DIR}/*.mp3"):
        stat = os.stat(file)
        filename = os.path.basename(file)
        creation_time = datetime.datetime.fromtimestamp(stat.st_ctime, datetime.timezone.utc) 
        episodes.append({
            "filename": filename,
            "text": filename.replace(".mp3", ".txt"),
            "creation_time": creation_time,
        })
    return episodes


if __name__ == "__main__":
    Path(f"{ASSETS_DIR}/index.html").write_text(homepage())
    Path(f"{ASSETS_DIR}/rss.xml").write_bytes(rss_feed())
