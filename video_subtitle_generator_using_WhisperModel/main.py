import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import shutil
from tkinter import filedialog as fd
import subprocess
from pytube import YouTube
        
class DownloadManager:
    video_url = None

    def download_video(self):
        try:
            streams = YouTube(self.video_url).streams.filter(progressive=True, subtype="mp4", resolution="360p")
            if len(streams) == 0:
                raise Exception("No suitable stream found for this YouTube video!")
            print("Downloading...")
            streams[0].download(filename="video.mp4")
            print("Download completed.")
        except Exception as e:
            messagebox.showerror("Error", e)

    def browse_file(self):
        src_path = fd.askopenfilename()
        shutil.copy(src_path, "./video.mp4")
        print("File Imported")
        
class SubtitleManager:
    def extract_audio(self):
        subprocess.run(["python", "extract.py"])
        print("Audio Extracted")

    def write_subtitles(self):
        subprocess.run(["python", "srt_creator.py"])
        print("Subtitles Written")

    def subbed_video(self):
        subprocess.run(["python", "subbed_video.py"])
        print("Video With Subtitle")

    def lsten_video(self):
        subprocess.run(["python", "listen.py"])
        print("Audio Broken Down to Sentences")
                
class ButtonClass(DownloadManager):
    rt=None
    global entry    
    def __init__(self, root):
        self.rt = root

    def caller(self):
        obj = SubtitleManager()
        obj.extract_audio()
        obj.lsten_video()
        obj.write_subtitles()
        obj.subbed_video()

    def dn(self):
        self.video_url = entry.get()
        self.download_video()

    def button(self):

        self.rt.title("Auto Subtitle Generator")

        dnld = ttk.Button(self.rt, text = "Download", command=self.dn)
        dnld.pack()
		
        label = ttk.Label(self.rt, text = "or")
        label.pack()
		
        brwse = ttk.Button(self.rt, text="Browse", command=self.browse_file)
        brwse.pack()

        run_the_model = ttk.Button(self.rt, text="Run Whisper", command=self.caller)
        run_the_model.pack(pady=10)

rt = tk.Tk()
entry = ttk.Entry(rt, width=50)
entry.pack(pady=10)
btn_obj = ButtonClass(rt)
btn_obj.button()
rt.mainloop()
