import auditok
from pathlib import Path
from extract import audio_directory

def segment_audio(audio_name):
  audio_regions = auditok.split(audio_name,
    min_dur=2,     # minimum duration of a valid audio in seconds
    max_dur=8,       # maximum duration of an audio segment
    max_silence=0.8, # maximum duration of tolerated continuous silence within an event
    energy_threshold=55, # threshold of detection
    sampling_rate=16000
  )
  for i, r in enumerate(audio_regions):
    filename = r.save(audio_name[:-4]+f'_{r.meta.start:08.3f}-{r.meta.end:08.3f}.wav')

segment_audio(audio_directory+'/temp.wav')

segments = [f for f in Path(audio_directory).glob(f'temp_*.wav')]
# display(Audio(str(segments[0])))
