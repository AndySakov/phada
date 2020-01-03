from flask import *
from werkzeug.utils import secure_filename
from api import Admin, ServeData
from threading import Thread
import api
import numpy as np
import pandas as pd
import sys, os

def flush_upcoming():
    xoxo = ServeData().fetchUpcoming()
    now = api.BuildStandardDate()
    year = now.split(" ")[-1]
    now = pd.to_datetime(now)
    for i in xoxo:
        then = pd.to_datetime("%s %s %s" % ( i[-2], i[-1], year ) )
        diff = now-then
        if (diff.days >= 0):
            api.popId('upcoming', i[0])
        else:
            continue
    return True

flush_upcoming()

def threader():
    while True:
        flush_upcoming()

# th1 = Thread(target = threader, args = ())
# th1.start()

app = Flask(__name__)
app.config['SECRET_KEY'] = b'XM34nJNN$NIJ'
__PATH__ = os.path.realpath("")

@app.route("/")
def landing():
    data = ServeData(fetchall = True)
    return render_template("index.html", data = data)

@app.route("/gallery")
def gallery():
    data = ServeData()
    cat = data.get_unique_cat()
    return render_template("gallery.html", cat = cat , gallery = data.fetchGallery())

@app.route("/music")
def download():
    data = ServeData()
    music = data.fetchMusic()
    return render_template("download.html", music = music , album = data.fetchAlbum())

@app.route("/blog")
def blog():
    data = ServeData()
    blog = data.fetchBlog()
    return render_template("blog.html", blog = blog)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/backend-contact", methods = ['GET', 'POST'])
def func_contact():
    if ('n' in request.form):
        name = request.form['n']
    else:
        name = 'anonymous'
    email = request.form['e']
    phone = request.form['p']
    msg = request.form['m']
    res = api.contact(email, phone, msg, name)
    if (res == True):
        flash("Your message has been sent")
    else:
        flash("There was an error in your request. Please try again later")
    return redirect(url_for('contact'))

@app.route("/upload", methods = ['GET', 'POST'])
def upload():
    return render_template('upload.html')

@app.route("/upload-song", methods = ['POST'])
def upload_song():
    name = request.form['name']
    artist = request.form['artist']
    _file = request.files['file']
    fname = "%s-%s-%s" % (name, artist, _file.filename)
    os.chdir("static/music")
    _file.save(fname)
    os.chdir(__PATH__)
    if ('lyrics' in request.form):
        lyrics = request.form['lyrics']
    else:
        lyrics = "No Quotable Lyrics"
    
    res = Admin().upload_song(name, artist, fname, lyrics)
    
    return redirect(url_for('upload'))

@app.route("/upload-picture", methods = ['GET', 'POST'])
def upload_picture():
    category = request.form['name']
    category = category.replace(" ", "")
    _file = request.files['file']
    fname = secure_filename(_file.filename)
    os.chdir("static/gallery")
    _file.save(fname)
    os.chdir(__PATH__)
    res = Admin().upload_to_gallery(fname, category)
    return redirect(url_for('upload'))

@app.route('/upload-blog-content', methods = ['POST'])
def upload_article():
    name = request.form['name']
    _file = request.files['file']
    fname = secure_filename(_file.filename)
    os.chdir("static/blog")
    _file.save(fname)
    os.chdir(__PATH__)
    if ('content' in request.form):
        content = request.form['content']
    else:
        content = ""

    res = Admin().upload_to_blog(fname, name, content)

    return redirect(url_for('upload'))

@app.route("/upload-event", methods = ['POST'])
def upload_event():
    name = request.form['name']
    info = request.form['info']
    date = request.form['date']

    res = Admin().upload_event(name, info, date)

    return redirect(url_for('upload'))

@app.route("/upload-review", methods = ['POST'])
def upload_review():
    name = request.form['name']
    bio = request.form['bio']
    rev = request.form['rev']

    res = Admin().upload_review(rev, name, bio)

    return redirect(url_for('upload'))

@app.route("/listen")
def play():
    mus = request.args['mus']
    lyr = request.args['lyr'] 
    art = request.args['art']
    name = request.args['name']
    return render_template("musicplay.html", mus = mus, lyr = lyr, art = art, name = name)

if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug = True)