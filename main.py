from time import time
from fastapi import FastAPI, __version__
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Form
import random
import os
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


from hardstorage import DATA

from Levenshtein import distance as lev

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# List of MP3 files in the "static" directory
#mp3_files = [file for file in os.listdir("static") if file.endswith(".mp3")]

song_choose = -1

@app.get("/")
def root(request: Request):
    global song_choose
    song = random.randint(1,25)
    song_id_spec = random.randint(1,5)

    file_path = f"{song}/{song_id_spec}.mp3"
    
    song_choose = song
    return templates.TemplateResponse("index.html", {"request": request, "mp3_file": file_path})

@app.post("/check_song")
def check_song(title: str = Form(...), composer: str = Form(...),obd: str = Form(...)):
    global song_choose
    good_out = DATA.get(str(song_choose),"aa")
    # {'comp': 'Peter Iljič Čajkovski', 'title': 'Labodje jezero', 'obdobje': 'ROMANTIKA'}
    
    
    
    distance_comp = lev(composer, good_out['comp'])
    distance_title = lev(title, good_out['title'])
    distance_obd = lev(obd, good_out['obdobje'].lower())
    
    
    return {"feedback": f"{good_out}, napake: {distance_comp} {distance_title} {distance_obd}"}

@app.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}