import time
import sys
import Connection as Cn
import Character as Ch
import Dialogues as Dg
import Language as Lang
import keyboard as kb
import Mechanics as Mh

# Login----------------------------------------------------------
login = 0
path = 0
success_or_fail = ''
print('Enter your Language / Entre com sua linguagem')
print('[0 - English] / [1 - Português-Brasil]')
while True:
    if kb.is_pressed('0'):
        language = 0
        kb.press('backspace')
        break
    elif kb.is_pressed('1'):
        language = 1
        kb.press('backspace')
        break
time.sleep(0.3)
Dg.clear()
name, Location = Cn.login(login, language)
race = Ch.choose_race(name, language)
RaceText, RaceLang, ClassText, ClassLang = race
ReloadLocation = Cn.select_function('name', f"Name = '{name}'")
Location = ReloadLocation[0][3]
# ---------------------------------------------------------------

# Race-----------------------------------------------------------
if Location == 0:
    Dg.clear()
    race = Ch.choose_race(name, language)
RaceText, RaceLang, ClassText, ClassLang = race
# ---------------------------------------------------------------

# FirstLocation FOREST-------------------------------------------
if Location == 1:
    time.sleep(1)
    Dg.clear()
    where = f"dialogue_location = 'location_one' AND lang = '{language}'"
    query = Cn.select_function('dialogues', where)
    Dg.dialogue_system(query, name, 'DONKOR')
    while True:
        if kb.is_pressed('0'):
            result = Cn.update_location(name, 2)
            ReloadLocation = Cn.select_function('name', f"Name = '{name}'")
            Location = ReloadLocation
            break
        elif kb.is_pressed('1'):
            path = 1
            break
        elif kb.is_pressed('2'):
            path = 1
            break

# SecondLocation FOREST SOUTH-WEST------------------------------
Location = ReloadLocation[0][3]
if Location == 2:
    time.sleep(0.5)
    Dg.clear()
    where = f"dialogue_location = 'location_two' AND lang = '{language}'"
    query = Cn.select_function('dialogues', where)
    Dg.dialogue_system(query, name, 'DONKOR')
    while True:
        if kb.is_pressed('0'):
            time.sleep(0.5)
            Dg.clear()
            d20_pass = [0, 20, 25, 35]
            where = f"dialogue_location = 'disperse_fog' AND lang = '{language}'"
            query = Cn.select_function('dialogues', where)
            success_or_fail = Mh.prepare_for_skill_test(name, 'ARCANE', language, ClassText, d20_pass, Lang.location_test_skill,
                                      1, 5, Lang.second_location_weapons, query)
            break
        elif kb.is_pressed('1'):
            time.sleep(0.5)
            Dg.clear()
            d20_pass = [0, 20, 25, 35]
            where = f"dialogue_location = 'follow_intuition' AND lang = '{language}'"
            query = Cn.select_function('dialogues', where)
            success_or_fail = Mh.prepare_for_skill_test(name, 'INTUITION', language, ClassText, d20_pass, Lang.location_test_skill,
                                      1, 6, Lang.second_location_weapons, query)
            break
        elif kb.is_pressed('2'):
            time.sleep(0.5)
            Dg.clear()
            d20_pass = [0, 20, 25, 35]
            where = f"dialogue_location = 'climb_tree' AND lang = '{language}'"
            query = Cn.select_function('dialogues', where)
            success_or_fail = Mh.prepare_for_skill_test(name, 'ACROBATIC', language, ClassText, d20_pass, Lang.location_test_skill,
                                      1, 3, Lang.second_location_weapons, query)
            break
        elif kb.is_pressed('3'):
            time.sleep(0.5)
            Dg.clear()
            d20_pass = [0, 20, 25, 35]
            where = f"dialogue_location = 'run_forward' AND lang = '{language}'"
            query = Cn.select_function('dialogues', where)
            success_or_fail = Mh.prepare_for_skill_test(name, 'ATHLETICS', language, ClassText, d20_pass, Lang.location_test_skill,
                                      1, 2, Lang.second_location_weapons, query)
            break
    time.sleep(0.5)
    Dg.clear()
    where = f"dialogue_location = 'location_two2' AND lang = '{language}' AND success = '0'"
    query = Cn.select_function('dialogues', where)
    Dg.dialogue_system(query, name, 'KAEN')
    while True:
        if kb.is_pressed('space'):
            break
    if success_or_fail:
        Dg.clear()
        where = f"dialogue_location = 'location_two2' AND lang = '{language}' AND success = '1'"
        query = Cn.select_function('dialogues', where)
        Dg.dialogue_system(query, name, 'KAEN')
        while True:
            if kb.is_pressed('space'):
                break
    else:
        Dg.clear()
        where = f"dialogue_location = 'location_two2' AND lang = '{language}' AND success = '2'"
        query = Cn.select_function('dialogues', where)
        Dg.dialogue_system(query, name, 'KAEN')
        while True:
            if kb.is_pressed('space'):
                break
    Dg.clear()
    where = f"dialogue_location = 'location_two2' AND lang = '{language}' AND success = '3'"
    query = Cn.select_function('dialogues', where)
    Dg.dialogue_system(query, name, 'KAEN')
