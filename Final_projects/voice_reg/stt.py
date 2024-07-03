'''Author: Artashes Sardaryan
About: importing AI , organize listening'''
import vosk
import sys
import sounddevice as sd
import queue
import json

model = vosk.Model('model_small')
samplerate = 16000
device = 1

q = queue.Queue()


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def va_listen(callback):
    '''listening'''
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                            channels=1, callback=q_callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                callback(json.loads(rec.Result())["text"])
            elif data =="заверши":
                break
            # else:
            #     print(rec.PartialResult()) 