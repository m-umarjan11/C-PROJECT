from base64 import b64encode
import subprocess
def combine_subtitles(input_file,  subtitle_file, output_file):
	command = ["ffmpeg", "-i", input_file, "-vf", f"subtitles={subtitle_file}", output_file]
	subprocess.run(command)

combine_subtitles('./video.mp4', './video.srt', './video_subbed.mp4')
