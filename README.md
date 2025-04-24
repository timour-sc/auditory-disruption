# AuditoryDisruption Project

This project extracts audio from video, analyzes disruption levels, and applies dynamic visual effects based on audio turbulence.

## Folder Structure
- `/videos/`: Original input .mp4 files
- `/audio/`: Extracted .wav files
- `/outputs/`: Final processed videos
- `/audio_processing/`: Audio extraction and analysis code
- `/effects/`: Visual effect functions
- `/utils/`: Helper functions
- `main_pipeline.py`: Main project runner
- `config.json`: Folder paths and settings

## How to Run
1. Place a .mp4 file inside `/videos/`.
2. Run:

```bash
python main_pipeline.py
