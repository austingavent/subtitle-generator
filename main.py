import os
import subprocess
import re
import time
from googletrans import Translator

start_time = time.time()

# Initialize Google Translator
translator = Translator()

# Base directories
# base_dir = "/Volumes/SanDisk/shinchan_whisper1"
# output_base_dir = "/Volumes/SanDisk/subtitles"
# test_base_dir = "/Volumes/SanDisk/test"

base_dir = "/app/data"
output_base_dir = "/app/data/subtitles"

# Ensure output directories exist
os.makedirs(output_base_dir, exist_ok=True)

def translate_text_with_googletrans(text):
    """Translate Japanese text using Google Translate."""
    try:
        translated_text = translator.translate(text, src="ja", dest="en").text
        return translated_text
    except Exception as e:
        print(f"Error translating text '{text}': {e}")
        return "unknown_episode"

def clean_filename(file_name):
    """Generate cleaned and translated file names."""
    # Extract the date portion
    date_match = re.search(r"\[\d{4}-\d{2}-\d{2}\]", file_name)
    date = date_match.group(0) if date_match else ""

    # Extract the Japanese name
    japanese_name_match = re.search(r"＃\d+-\d+\s+([^\[]+)", file_name)
    japanese_name = japanese_name_match.group(1).strip() if japanese_name_match else "unknown"

    # Translate the Japanese name
    translated_name = translate_text_with_googletrans(japanese_name)

    # Construct the cleaned file name
    return f"{translated_name} {date}".strip()

def process_videos(base_dir):
    """Run Whisper to generate subtitles and merge them with the videos."""
    for root, _, files in os.walk(base_dir):
        for file_name in files:
            if file_name.endswith(".mp4"):
                video_path = os.path.join(root, file_name)

                # Generate cleaned filename
                cleaned_name = clean_filename(file_name)
                target_dir = os.path.join(output_base_dir, cleaned_name)
                os.makedirs(target_dir, exist_ok=True)

                # Move the video to the target directory with the cleaned name
                target_video_path = os.path.join(target_dir, f"{cleaned_name}.mp4")
                os.rename(video_path, target_video_path)
                print(f"Video moved to: {target_video_path}")

                # Run Whisper for transcription
                whisper_command = [
                    "whisper", target_video_path,
                    "--language", "Japanese",
                    "--task", "translate",
                    "--model", "medium",
                    "--output_dir", target_dir,
                    "--device", "cuda"
                ]
                try:
                    subprocess.run(whisper_command, check=True)
                    print(f"Whisper transcription complete for: {target_video_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Error processing video: {e}")
                    continue
                # Merge subtitles with the video
                # Merge subtitles with the video
                base_name = os.path.splitext(file_name)[0]
                subtitle_path = os.path.join(target_dir, f"{cleaned_name}.srt")
                merged_video_path = os.path.join(target_dir, f"{cleaned_name}_merged.mp4")
                if os.path.exists(subtitle_path):
                    # Ensure UTF-8 encoding for subtitle file
                    ensure_utf8_encoding(subtitle_path)

                    # Sanitize subtitle path for FFmpeg
                    sanitized_subtitle_path = f'"{subtitle_path}"'  # Wrap in double quotes

                    # FFmpeg merge command
                    ffmpeg_merge_command = [
                        "ffmpeg", "-i", target_video_path,
                        "-vf", f"subtitles={sanitized_subtitle_path}",
                        "-c:a", "copy", merged_video_path
                    ]
                    try:
                        subprocess.run(ffmpeg_merge_command, check=True)
                        print(f"Merged video saved to: {merged_video_path}")
                    except subprocess.CalledProcessError as e:
                        print(f"Error merging subtitles: {e}")


def ensure_utf8_encoding(file_path):
    with open(file_path, "rb") as f:
        content = f.read().decode("utf-8", errors="ignore")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python main.py <directory>")
    #     sys.exit(1)

    # Get the directory from the command-line arguments
    #directory = sys.argv[1]
    process_videos(base_dir)