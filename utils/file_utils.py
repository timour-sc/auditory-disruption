import os
import subprocess
import json

def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_video_rotation(video_path):
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream_tags=rotate',
            '-of', 'json', video_path
        ], capture_output=True, text=True)

        output = result.stdout
        if output:
            metadata = json.loads(output)
            streams = metadata.get('streams', [])
            if streams and 'tags' in streams[0] and 'rotate' in streams[0]['tags']:
                rotation = int(streams[0]['tags']['rotate'])
                return rotation
        return 0  # Default no rotation
    except Exception as e:
        print(f"⚠️ Could not read rotation metadata for {video_path}: {e}")
        return 0
