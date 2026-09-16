import subprocess
import json
import logging

logging.basicConfig(filename="logs.log", encoding="utf-8", level=logging.DEBUG)


def get_transcripts(titles, subpath):

    for title, url in titles.items():
        try:
            subprocess.run(
                [
                    "yt-dlp",
                    "--no-check-certificate",
                    "--skip-download",
                    "--write-subs",
                    f'-o "transcripts/{subpath}/{"_".join(title.split())}.%(ext)s"',
                    f"{url}",
                ],
                shell=True,
            )
        except Exception as e:
            logging.error(f"Could not run subprocess on -> {title}:{url}")
            continue


def get_audio(titles, subpath):
    """Get mp3 files.
    Use this in the event there are no subtitles for a video
    We will need to convert the mp3 to text using text to audio
    """
    for title, url in titles.items():
        try:
            subprocess.run(
                [
                    "yt-dlp",
                    "--no-check-certificate",
                    "--extract-audio",
                    "--audio-format",
                    "mp3",
                    "--audio-quality",
                    "0",
                    f'-o "audio/{subpath}/{"_".join(title.split())}.%(ext)s"',
                    f"{url}",
                ],
                shell=True,
            )
        except Exception as e:
            logging.error(f"Could not run subprocess on -> {title}:{url}")
            continue


if __name__ == "__main__":
    title_names_file = "data/TheoreticalBullshit_titles.json"
    with open(title_names_file) as f:
        data = json.load(f)

    get_audio(titles=data, subpath="TheoreticalBullshit")
