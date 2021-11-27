import time
import keyboard as kb
import Character as Ch
import Connection as Cn
import Dialogues as Dg
import Language as Lang
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

# Race Creation (Only if player log out after create account and don't choose the race)
if Location == 0:
    Dg.clear()
    race = Ch.choose_race(name, language)
RaceText, RaceLang, ClassText, ClassLang = race

# FirstLocation FOREST-------------------------------------------
if Location == 1:
    # Will select the dialogues from database where location match's with location_one and lang choosed by the player
    time.sleep(1)
    Dg.clear()
    where = f"dialogue_location = 'location_one' AND lang = '{language}'"
    query = Cn.select_function('dialogues', where)
    Dg.dialogue_system(query, name, 'DONKOR')
    while True:
        if kb.is_pressed('0'):
            result = Cn.update_function('name', 'Location = 2', f"Name = '{name}'")
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
    # Will select the dialogues from database where location match's with location_two and lang choosed by the player
    time.sleep(0.5)
    Dg.clear()
    where = f"dialogue_location = 'location_two' AND lang = '{language}'"
    query = Cn.select_function('dialogues', where)
    Dg.dialogue_system(query, name, 'DONKOR')
    while True:
        if kb.is_pressed('0'):
            time.sleep(0.5)
            Dg.clear()
            # will set d20_pass values for critical failure 0 to 20, failure 20 to 25, success 25 to 35 or
            # critical success above 35 in d20
            d20_pass = [0, 20, 25, 35]
            # Will select the dialogues from database where location match's with disperse_fog and lang
            # choosed by the player
            where = f"dialogue_location = 'disperse_fog' AND lang = '{language}'"
            query = Cn.select_function('dialogues', where)
            # will set debuff index and time for display if the player get critical failure in d20
            debuff = [1, 6]
            # will set the arguments for skill test and return 1 if player get critical success or success in d20
            # and return 2 if player get failure or critical failure in d20
            success_or_fail = Mh.prepare_for_skill_test(name, 'ARCANE', language, ClassText, d20_pass,
                                                        Lang.test_skill_language,
                                                        1, 5, Lang.second_location_weapons, query, 1, debuff)
            break
        elif kb.is_pressed('1'):
            time.sleep(0.5)
            Dg.clear()
            d20_pass = [0, 20, 25, 35]
            where = f"dialogue_location = 'follow_intuition' AND lang = '{language}'"
            query = Cn.select_function('dialogues', where)
            debuff = [2, 6]
            success_or_fail = Mh.prepare_for_skill_test(name, 'INTUITION', language, ClassText, d20_pass,
                                                        Lang.test_skill_language,
                                                        1, 6, Lang.second_location_weapons, query, 1, debuff)
            break
        elif kb.is_pressed('2'):
            time.sleep(0.5)
            Dg.clear()
            d20_pass = [0, 20, 25, 35]
            where = f"dialogue_location = 'climb_tree' AND lang = '{language}'"
            query = Cn.select_function('dialogues', where)
            debuff = [3, 6]
            success_or_fail = Mh.prepare_for_skill_test(name, 'ACROBATIC', language, ClassText, d20_pass,
                                                        Lang.test_skill_language,
                                                        1, 3, Lang.second_location_weapons, query, 1, debuff)
            break
        elif kb.is_pressed('3'):
            time.sleep(0.5)
            Dg.clear()
            d20_pass = [0, 20, 25, 35]
            where = f"dialogue_location = 'run_forward' AND lang = '{language}'"
            query = Cn.select_function('dialogues', where)
            debuff = [1, 6]
            success_or_fail = Mh.prepare_for_skill_test(name, 'ATHLETICS', language, ClassText, d20_pass,
                                                        Lang.test_skill_language, 1, 2, Lang.second_location_weapons,
                                                        query, 1, debuff)
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
    # Will select the dialogues from database where location match's with location_two2, lang choosed by the player
    # and success is 3
    where = f"dialogue_location = 'location_two2' AND lang = '{language}' AND success = '3'"
    query = Cn.select_function('dialogues', where)
    Dg.dialogue_system(query, name, 'KAEN')
    while True:
        if kb.is_pressed('space'):
            break
    Dg.clear()
    # Will call the function combat from Mechanics by setting the arguments
    d20_pass = [0, 20, 25, 35]
    Mh.combat(name, 'Ghast', 120, language, d20_pass, 50)
