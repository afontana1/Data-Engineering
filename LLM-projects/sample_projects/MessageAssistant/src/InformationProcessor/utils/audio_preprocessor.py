import os
import subprocess
import tempfile
import librosa
import torch
from transformers import pipeline
import soundfile as sf


class AudioProcessor:
    def __init__(self, model="openai/whisper-medium.en"):
        self.model = model
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            chunk_length_s=30,
            device=self.device,
        )

    @staticmethod
    def convert_to_wav(input_file):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            temp_file_path = tmp_file.name

        command = ['ffmpeg', '-y', '-i', input_file, '-acodec', 'pcm_s16le', '-ar', '32000', temp_file_path]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Check if there was an error
        if result.returncode != 0:
            print(f"Error occurred while converting {input_file}: {result.stderr}")
        else:
            print("Conversion completed successfully!")  # Your custom message

        return temp_file_path

    def process_audio_file(self, file_path):
        try:

            # if file_path.lower().endswith('.m4a'):
            file_path = self.convert_to_wav(file_path)      # Check the file extension and convert if necessary

            audio, sample_rate = sf.read(file_path)

            # if sample_rate != 32000:
            #     audio = librosa.resample(audio, sample_rate, 32000)

            audio_duration = len(audio) / 32000     # get the length of the audio in seconds

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                sf.write(tmp_file.name, audio, 32000)
                temp_file_path = tmp_file.name

            prediction = self.pipe(temp_file_path)["text"]
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        except Exception as exception:
            print(f"Error processing file {file_path}: {exception}")
            prediction = None
            audio_duration = None

        # finally:
        #     if os.path.exists(temp_file_path):
        #         os.remove(temp_file_path)

        return prediction, audio_duration


# if __name__ == "__main__":
#     ap = AudioProcessor()
#     print(ap.process_audio_file(r"C:\Users\cmazz\PycharmProjects\UntitledAssitantTool\inputdata\diversityinprwav.wav"))