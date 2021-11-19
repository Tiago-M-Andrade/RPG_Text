import time
from os import system, name
import sys
import keyboard
import Language as Lang
import Connection as Cn
import simpleaudio as sa
import random
from termcolor import colored


def clear():
    # for windows the name is 'nt'
    if name == 'nt':
        _ = system('cls')

    # and for mac and linux, the os.name is 'posix'
    else:
        _ = system('clear')


def text_speech(texts, delay):
    for text in texts:
        sys.stdout.flush()
        sys.stdout.write(text)
        if keyboard.is_pressed('space'):
            time.sleep(0.02)
        elif keyboard.is_pressed('enter'):
            clear()
            sys.stdout.flush()
            sys.stdout.write(texts)
            time.sleep(0.1)
            break
        else:
            time.sleep(delay)


def dialogue_system(dialogue, character_name, search_name):
    lang_texts = dialogue
    i = 0
    for cod, location, text, lang, success in lang_texts:
        i += 1
        if '{}' in text:
            text_speech(text.format(colored(character_name, 'red')), 0.02)
        elif search_name in text:
            text_speech(text.replace(search_name, "{}").format(colored(search_name, 'green')), 0.02)
        else:
            text_speech(text, 0.02)
        if (i) == len(lang_texts):
            break
        while True:
            if keyboard.is_pressed('space'):
                clear()
                break
