import streamlit as st
import os
import logging
import timeit
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from alive_progress import alive_bar

# Setting terminal colors
RED = "\033[31;1m"
GREEN = "\033[32;1m"
CIANO = "\033[36;1m"
RESET = "\033[0;0m"

# Setting the logging configurations
logging.basicConfig(
    format="%(asctime)s - audiototxt.py - %(message)s", level=logging.DEBUG
)

# Get start time
starttime = timeit.default_timer()
logging.debug(f"⏱ {GREEN}Start time: {starttime}{RESET}")


def save_audio_file(audio_bytes, filename):
    """
    Save audio bytes to a file with the specified extension.

    :param audio_bytes: Audio data in bytes
    :param file_extension: The extension of the output audio file
    :return: The name of the saved audio file
    """
    file_name = f"{filename}"

    with open(f"{file_name}", "wb") as f:
        f.write(audio_bytes)

    return file_name


def create_wav_files(audio_file):

    # Audio files
    AUDIO_SRC = audio_file
    AUDIO_DST = f"{AUDIO_SRC}.wav"

    # Converting audio to wav
    logging.debug(f"{GREEN}Coverting audio to .wav file.{RESET}")
    audio = AudioSegment.from_mp3(AUDIO_SRC)
    audio.export(AUDIO_DST, format="wav")

    audio = AudioSegment.from_file(AUDIO_DST, "wav")
    segment_size = 30000

    logging.debug(f"{GREEN}Segmenting audio file.{RESET}")

    part = make_chunks(audio, segment_size)
    part_audio = []

    for i, part in enumerate(part):
        part_name = f"part{i}.wav"
        part_audio.append(part_name)
        part.export(part_name, format="wav")
        logging.debug(f"Audio segment created: {part_name}")
    return part_audio


def transcript_audio(name_audio):
    """This function trascript the audio file
    to string.

    Args:
        name_audio (str): name of audio file

    Returns:
        str : result of audio content in text string
    """
    # Select the audio file
    r = sr.Recognizer()
    with sr.AudioFile(name_audio) as source:
        audio = r.record(source)  # Reading audio file

    try:
        logging.debug(f"Google Speech Recognition: Transcript {name_audio}")
        text = r.recognize_google(audio, language="en")
    except Exception as e:
        raise (e)
    return text


def convert_files(parts, filename):
    # Trascription of audios segments
    text = ""
    with alive_bar(len(parts), dual_line=True, title="Transcription") as bar:
        progress_text = "File Chunk {}. Please wait."
        my_bar = st.progress(0, text=progress_text)
        for file_chunk, part in enumerate(parts):
            text = f"{text} {transcript_audio(part)}"
            bar()
            my_bar.progress(file_chunk + 1, text=progress_text.format(file_chunk))
    logging.debug(f"{RED}Transcript of the audio file:{RESET}")

    directory = "transcripts"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Save data in a .txt file
    with open(f"{directory}\\{filename}.txt", "w") as file:
        file.write(text)
    logging.debug(f"📝 {GREEN}Created audio.txt file{RESET}")

    # Cleaning segment audios
    logging.debug(f"🗑 {GREEN} Cleaning segment audios.{RESET}")
    os.system("del -f part*")
    os.system("del /S *.mp3")
    os.system("del /S *.wav")

    # Show the the time of script
    logging.debug(f"⏱ {GREEN}End time: {timeit.default_timer() - starttime}{RESET}")


def main():
    st.title("Speech to Text Converter")
    st.write("Upload an audio file and convert it to text.")

    uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])
    file_saved = None
    if uploaded_file is not None:
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type}
        st.write(file_details)

        file_saved = save_audio_file(
            uploaded_file.read(),
            filename=uploaded_file.name,
        )
    if file_saved:
        parts = create_wav_files(uploaded_file.name)
        with st.spinner("converting files...."):
            convert_files(parts=parts, filename=uploaded_file.name)

            st.balloons()


if __name__ == "__main__":
    main()
