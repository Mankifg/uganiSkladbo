from time import time
from fastapi import FastAPI, __version__
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Form
import random
import os
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Cookie, FastAPI

from hardstorage import DATA

from Levenshtein import distance as lev

from discord_webhook import DiscordWebhook

URL = "https://discord.com/api/webhooks/1204521413768388699/cHMP6fDBZs_IoEZjo0TPfTe3Yw7GGFuTfJDmDq0zjSGHwI1re8iKymP6P372hZUBLkQJ"


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

song_choose = -1


@app.get("/")
def root(request: Request):
    global song_choose
    song = random.randint(1, 25)

    file_path = f"{song}/{random.randint(1, 5)}.mp3"

    song_choose = song
    return templates.TemplateResponse(
        "index.html", {"request": request, "mp3_file": file_path,"cook":song_choose}
    )


@app.post("/check_song")
def check_song(titleS: str = Form(...), composerS: str = Form(...), obdS: str = Form(...),cookS: str = Form(...)):
    good_out = DATA.get(str(cookS), "aa")
    # {'comp': 'Peter Iljič Čajkovski', 'title': 'Labodje jezero', 'obdobje': 'ROMANTIKA'}


    distance_comp = lev(composerS, good_out["comp"])
    distance_title = lev(titleS, good_out["title"])
    distance_obd = lev(obdS, good_out["obdobje"].lower())
    errors = sum([distance_comp, distance_title, distance_obd])

    skladba = f"{good_out['comp']} : {good_out['title']} - {good_out['obdobje']} ({song_choose})"
    webhook = DiscordWebhook(
        url=URL,
        content=f"""[INFO] \nUser: ```{composerS}:{titleS}-{obdS}```
        Good:```{good_out['comp']}:{good_out['title']}-{good_out['obdobje']}={song_choose}```""",
    )

    response = webhook.execute()
   
    return {
        "feedback": f"{skladba}\nnapake: {errors}({distance_title},{distance_comp},{distance_obd})"
    }


@app.get("/ping")
async def ping():
    return {"res": "pong", "version": __version__, "time": time()}


@app.get("/tos")
async def tos():
    return """Z Uporabo te spletne strani se strinjate s Pogoji storitve (ToS).
            1. Spletna stran narejena za izobraževalne namene. 
            2. Ne odgovarjam za morebitne napačne povratne informacije. 
            3. Lahko beležimo podatke, ki ste jih vnesli za skadbo (naslov,skladatj ter obdobje)
            """
