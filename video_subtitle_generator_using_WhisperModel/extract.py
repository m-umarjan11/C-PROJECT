import subprocess
from pathlib import Path
from IPython.display import Audio, display

audio_directory = './temp_audio/'

def extract_audio(input_file):
	Path(audio_directory).mkdir(parents=True, exist_ok=True)
	audio_file = audio_directory+'/temp.wav'
	command = ["ffmpeg", "-i", input_file, "-ac", "1", "-ar", "16000","-vn", "-f", "wav", audio_file]
	subprocess.run(command)

extract_audio('video.mp4')
display(Audio(audio_directory+'/temp.wav')) 
