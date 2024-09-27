import pytube
import os
import moviepy.editor as mp
import speech_recognition as sr

# Function to download audio from a YouTube video
def download_audio(youtube_link, audio_name):
    youtube = pytube.YouTube(youtube_link)
    audio_stream = youtube.streams.filter(only_audio=True).first()
    audio_file = audio_stream.download('.', filename=audio_name)
    # return audio_file

# Function to transcribe audio from a video file
def transcribe_audio(audio_file, output_file):
    # Convert MP3 to WAV
    audio = mp.AudioFileClip(audio_file)
    audio.write_audiofile("temp_audio.wav")

    # Transcribe the audio
    recognizer = sr.Recognizer()
    with sr.AudioFile("temp_audio.wav") as source:
        audio = recognizer.record(source)
    transcript = recognizer.recognize_sphinx(audio)
    print(transcript)

    # Save the transcript to the output file
    with open(output_file, "w") as f:
        f.write(transcript)

    # Clean up: delete the temporary WAV file
    os.remove("temp_audio.wav")
    os.remove("custom_audio.mp3")

def transcriptManually(v_id):
    s='http://youtube.com/watch?v='
    yt_video_link= s+v_id
    print(yt_video_link)
    download_audio(yt_video_link,'custom_audio.mp3')
    output_file = "transcript.txt"
    transcribe_audio('./custom_audio.mp3', output_file)
    print(yt_video_link)
    # print(output_file)
    return output_file
    
# transcriptManually('https://www.youtube.com/watch?v=9esCA8_EPeY')




