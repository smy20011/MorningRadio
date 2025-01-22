from flask import Flask, render_template, send_from_directory, request, Response
from tzlocal import get_localzone
from feedgen.feed import FeedGenerator
import glob
import os
import datetime
import argparse

app = Flask(__name__)

PODCAST_TITLE = "Morning Routine"
PODCAST_DESCRIPTION = "Programmatically Generated Podcast"
ASSETS_DIR = "assets"  # Directory where your MP3 files are stored

@app.route("/")
def index():
    episodes = get_episodes()
    return render_template("index.html", episodes=episodes, podcast_title=PODCAST_TITLE, podcast_description=PODCAST_DESCRIPTION)

@app.route("/assets/<filename>")
def serve_assets(filename):
    return send_from_directory(ASSETS_DIR, filename)

@app.route("/rss")
def rss_feed():
    episodes = get_episodes()
    host = get_host()
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.title(PODCAST_TITLE)
    fg.link(href=f"http://{host}/")
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

def get_episodes():
    episodes = []
    for file in glob.glob("assets/*.mp3"):
        stat = os.stat(file)
        creation_time = datetime.datetime.fromtimestamp(stat.st_ctime, get_localzone())
        episodes.append({
            "filename": file,
            "creation_time": creation_time,
        })
    return episodes

def get_host():
    return request.host

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serve the podcast")
    parser.add_argument("--gen_time", dest="gen_time", default=None, required=False, help="Time (in your current timezone) to start generation")
    args = parser.parse_args()
    app.run(debug=True)
