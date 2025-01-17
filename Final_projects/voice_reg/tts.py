'''Author: Artashes Sardaryan
About: To found microphone and set defualt parametrs of assistent'''
import torch
import sounddevice as sd
import time

language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000
speaker = 'baya'
put_accent = True
device = torch.device('cpu')
model, _= torch.hub.load(repo_or_dir='snakers4/silero-models',
                      model='silero_tts',
                          language= language,
                          speaker = model_id)
model.to(device)
def va_speak(text: str):
    '''Asistent parameters'''
    audio =model.apply_tts(text =text,
            speaker = speaker,
            sample_rate=sample_rate,
            put_accent=put_accent,
            )
    # Asisstent speak spead 
    sd.play(audio, sample_rate * 1.05)
    time.sleep((len(audio) / sample_rate))
    sd.stop()