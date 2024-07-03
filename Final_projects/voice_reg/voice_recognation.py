''''Author: Artashes Sardaryan
About: include all files ,seting default commands'''
import config
import stt
import tts
from fuzzywuzzy import fuzz
import datetime
from num2words import num2words
import webbrowser
import random

print(f"{config.VA_NAME} (v{config.VA_VER}) начал свою работу ...")
tts.va_speak("привет я асистент ко-ко, что могу сделать для вас?")


def va_respond(voice: str):
    print(voice)
    if voice.startswith(config.VA_ALIAS):
        # contact the assistant
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak("Что?непонятная команда")
        else:
            execute_cmd(cmd['cmd'])


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str):
    if cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказывать анекдоты ..."
        text += "и открывать браузер"
        tts.va_speak(text)
        pass
    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        text = "Сейчас " + num2words(now.hour, lang='ru')  + " " + num2words(now.minute, lang='ru')
        tts.va_speak(text)

    elif cmd == 'joke':
        jokes = ['Как смеются программисты? ... ехе ехе ехе',
                 '— Почему ваши дети всё время ссорятся?— Конфликт версий, — отвечает программист.',
                 'Программист это машина для преобразования кофе в код',
                 'Один монитор—обычный программист,три монитора системный программист,четыре монитора охранник.']

        tts.va_speak(random.choice(jokes))

    elif cmd == 'open_browser':
        webbrowser.open_new('https://www.google.com/')

    elif cmd == 'End':
        exit()


#Start listening
stt.va_listen(va_respond)