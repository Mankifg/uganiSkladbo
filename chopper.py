from pathlib import Path
from pydub import AudioSegment
import random
import os

import shutil

shutil.rmtree("static/")

os.mkdir("static/")

VERSIONS_PER_ONE = 5

folders = [f"static/{i}/" for i in range(1, 26)]
for fold in folders:
    if not os.path.exists(fold):
        os.mkdir(fold)


for path in Path("./data").rglob("*.mp3"):

    path = str(path)
    path = path.replace("\\", "/")
    song_name = path.split("/")[-1][:-4]

    for i in range(VERSIONS_PER_ONE):
        song = AudioSegment.from_mp3(path)
        song_len = song.duration_seconds
        rand = random.randint(0, int(song_len - 30))
        song = song[rand * 1000 : (rand + 30) * 1000]
        new_path = f"static/{song_name}/{i+1}.mp3"
        print(new_path)
        song.export(new_path, format="mp3")
