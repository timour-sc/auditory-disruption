import subprocess
import os
import json

with open('config.json') as f:
    config = json.load(f)

def extract_audio(video_path, output_path):
    subprocess.run([
        'ffmpeg', '-i', video_path, '-q:a', '0', '-map', 'a', output_path, '-y'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
