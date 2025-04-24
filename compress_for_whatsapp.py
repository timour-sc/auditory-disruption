import os
import subprocess

# 📁 Folder setup
outputs_folder = "outputs"
whatsapp_folder = "whatsapp_ready"

os.makedirs(whatsapp_folder, exist_ok=True)

# WhatsApp maximum size (MB)
MAX_WHATSAPP_SIZE_MB = 16

# Helper to get file size in MB
def get_file_size(path):
    return os.path.getsize(path) / (1024 * 1024)

# Compress and resize video
def compress_video(input_path, output_path):
    subprocess.run([
        'ffmpeg', '-y',
        '-i', input_path,
        '-vf', 'scale=640:360',  # Resize to 640x360
        '-vcodec', 'libx264',
        '-crf', '30',             # Strong compression
        '-preset', 'veryfast',
        '-acodec', 'aac',
        output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def main():
    videos = [f for f in os.listdir(outputs_folder) if f.endswith('.mp4')]
    if not videos:
        print("❌ No videos found in 'outputs' folder.")
        return

    print(f"🚀 Compressing {len(videos)} videos...")

    for video in videos:
        input_path = os.path.join(outputs_folder, video)
        output_path = os.path.join(whatsapp_folder, video)

        original_size = get_file_size(input_path)

        # If already small, just copy it
        if original_size <= MAX_WHATSAPP_SIZE_MB:
            print(f"✅ {video} already under 16MB ({original_size:.2f}MB). Copying...")
            subprocess.run(['cp', input_path, output_path], shell=True)
        else:
            print(f"📦 Compressing {video} ({original_size:.2f}MB)...")
            compress_video(input_path, output_path)

        compressed_size = get_file_size(output_path)
        status = "✅ OK" if compressed_size <= MAX_WHATSAPP_SIZE_MB else "⚠️ Still too big"

        print(f"   → Final size: {compressed_size:.2f}MB {status}")

    print("\n🏁 Compression complete! Check the 'whatsapp_ready' folder.")

if __name__ == "__main__":
    main()
