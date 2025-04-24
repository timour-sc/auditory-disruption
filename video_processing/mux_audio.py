import subprocess

def mux_audio_back(video_path, audio_path, output_path):
    subprocess.run([
        'ffmpeg', '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
