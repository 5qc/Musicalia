from flask import Flask, render_template
from musicalia import Wd
from musicalia import wikipedia as Wp

import json
import re

app = Flask(__name__)
app.jinja_env.globals.update(enumerate = enumerate)
app.jinja_env.globals.update(str = str)

@app.route("/")
def home_page():
    return render_template("home.jinja")

@app.route("/album/")
@app.route("/album/<string:qid>")
def album_page(qid: str = "Q0"):
    if qid == "Q0": return render_template("album.jinja")
    
    data = Wd(qid)
    
    tracklist_data = data.claim("P658")
    tracklist = []
    # for x in tracklist_data:
    #     z = Wd(x)
    #     tracklist.append([z.label("en")])
    
    artist_data = data.claim("P175")
    artist = []
    for x in artist_data:
        artist.append( [x, Wd(x).label("en")] )
    
    wikipedia = Wp( data.sitelink("enwiki") )
    img = "https:" + wikipedia.image.group(1)
    
    data_attr = json.dumps(data.json, separators=(",", ":")).replace('"', '&quot;')
    return render_template("album.jinja",
                           data = data,
                           json_data = data_attr,
                           tracklist = tracklist,
                           artist = artist,
                           wikipedia = wikipedia,
                           img = img)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)