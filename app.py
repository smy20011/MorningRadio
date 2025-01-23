from feedgen.feed import FeedGenerator
from flask import Flask, render_template, Response, request, send_from_directory
import glob
import os
import datetime
import jinja2

PODCAST_TITLE = "Morning Routine"
PODCAST_DESCRIPTION = "Programmatically Generated Podcast"
ASSETS_DIR = "assets"  # Directory where your MP3 files are stored

app = Flask(__name__)


@app.route('/')
def homepage():
    episodes = get_episodes()
    return render_template("index.html", episodes=episodes, podcast_title=PODCAST_TITLE, podcast_description=PODCAST_DESCRIPTION)

@app.route("/rss.xml")
def rss_feed():
    episodes = get_episodes()
    host = request.host
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.title(PODCAST_TITLE)
    fg.link(href=host)
    fg.description(PODCAST_TITLE)

    for episode in episodes:
        fe = fg.add_entry()
        url = f"http://{host}/{episode['filename']}"
        fe.id(url)
        fe.title(f"{PODCAST_TITLE} {episode['creation_time'].strftime('%Y-%m-%d')}")
        fe.enclosure(url, 0,  'audio/mpeg')
        fe.published(episode['creation_time'])
        fe.guid(url)

    return Response(fg.rss_str(pretty=True), mimetype="application/rss+xml")

@app.route(f"/{ASSETS_DIR}/<name>")
def podcasts(name):
    return send_from_directory(ASSETS_DIR, name)

def get_episodes():
    episodes = []
    for filename in glob.glob(f"{ASSETS_DIR}/*.mp3"):
        stat = os.stat(filename)
        creation_time = datetime.datetime.fromtimestamp(stat.st_ctime, datetime.timezone.utc) 
        episodes.append({
            "filename": filename,
            "text": filename.replace(".mp3", ".txt"),
            "creation_time": creation_time,
        })
    return episodes


if __name__ == "__main__":
    app.run()
