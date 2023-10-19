import re
import datetime
import torch
import soundfile

from pathlib import Path
from extract import audio_directory

import whisper

model = whisper.load_model("base")

class SubtitleGenerator:
    def __init__(self, audio_directory, output_file):
        self.audio_directory = audio_directory
        self.output_file = output_file
        self.line_count = 0

    def clean_text(self, text):
        clean_text = re.sub(r'  ', ' ', text)
        clean_text = re.sub(r'\bi\s', 'I ', clean_text)
        clean_text = re.sub(r'\si$', ' I', clean_text)
        clean_text = re.sub(r'i\'', 'I\'', clean_text)
        return clean_text

    def get_srt_line(self, inferred_text, limits):
        sep = ','   
        d = str(datetime.timedelta(seconds=float(limits[0])))
        try:
            from_dur = '0' + str(d.split(".")[0]) + sep + str(d.split(".")[-1][:2])
        except:
            from_dur = '0' + str(d) + sep + '00'

        d = str(datetime.timedelta(seconds=float(limits[1])))
        try:
            to_dur = '0' + str(d.split(".")[0]) + sep + str(d.split(".")[-1][:2])
        except:
            to_dur = '0' + str(d) + sep + '00'
        return f'{str(self.line_count)}\n{from_dur} --> {to_dur}\n{inferred_text}\n\n'

    def get_subs(self):
        segments = sorted([f for f in Path(self.audio_directory).glob(f'temp_*.wav')])

        with open(self.output_file, 'w', encoding="utf-8") as out_file:
            for audio_file in segments:
                # Run OpenAI Whisper inference on each segemented audio file.
                speech, rate = soundfile.read(audio_file)
                 
                output_json = model.transcribe(speech)
                inferred_text = output_json['text']

                
                if len(inferred_text) > 0:
                    inferred_text = self.clean_text(inferred_text)
                else:
                    inferred_text = ''
                
                
                limits = audio_file.name[:-4].split("_")[-1].split("-")
                limits = [float(limit) for limit in limits]
                sb = self.get_srt_line(inferred_text, limits)
                print(sb)
                out_file.write(sb)
                out_file.flush()
                self.line_count += 1

sub_gen = SubtitleGenerator(audio_directory, './video.srt')
sub_gen.get_subs()

