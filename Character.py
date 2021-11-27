import time
import keyboard as kb
import Connection as Cn
import Language as Lang


def choose_race(name, language):
    """Verify if character race and class exists, if not then let the player choose

        Parameters:\n
        Name: get the player name logged in \n
        language: get the language choose by player \n
        Return:\n
        (Race like in DB), (Race in the language choose by player), (Class like in DB), (Class in the language choose
        by player \n
        for unpacking this function example: RaceDB, DisplayRace, ClassDB, DisplayClass = ChooseRace(name, language)
        """
    races = ['DWARF', 'ELF', 'GNOME', 'HALF-ELF', 'HALF-ORC', 'HALFLING', 'HUMAN']
    classes = ['BARBARIAN', 'BARD', 'CLERIC', 'DRUID', 'FIGHTER', 'MONK', 'PALADIN', 'RANGER', 'ROGUE', 'WIZARD',
               'MAGE']
    try:
        query = f"Name = '{name}'"
        result = Cn.select_function('race', query)
        cod, name_r, race_r, class_r = result[0]
        race = races.index(race_r)
        class_index = classes.index(class_r)
        race_language, choose_text, success, class_display, choose_text2 = Lang.race_language(language)
        return races[race], race_language[race], classes[class_index], class_display[class_index]
    except IndexError:
        display_races = str('')
        display_classes = str('')
        race_language, choose_text, success, class_display, choose_text2 = Lang.race_language(language)
        for i, race_lang in enumerate(race_language):
            display_races += str(f'{i} - {race_lang}  ')
        print(display_races)
        kb.press('backspace')
        race = int(input(choose_text))
        print(success.format(race_language[race]))
        for i2, class_lang in enumerate(class_display):
            display_classes += str(f'{i2} - {class_lang}  ')
        print(display_classes)
        class_input = int(input(choose_text2))
        Cn.insert_function('race', 'Name', 'Race', 'Class', name=f"{name}", race=f"{races[race]}",
                           clazz=f"{classes[class_input]}")
        character_base_attributes(name, language, class_display[class_input])
        return races[race], race_language[race], classes[race], class_display[race]


def character_base_attributes(name, language, race_lang):
    """Update character race attributes by using the the class index selected by the player in the function choose_race
    and display the base attributes before the game starts

            Parameters:\n
            Name: get the player name logged in \n
            language: get the language choose by player \n
            race_lang: get the race index where player choose the class in function choose_race
            Return:\n
            if successful, it will return true
            """
    # ['BARBARIAN', 'BARD', 'CLERIC', 'DRUID', 'FIGHTER', 'MONK', 'PALADIN', 'RANGER', 'ROGUE','WIZARD', 'MAGE']
    # Attributes Order str, dex, cons, int, wis, cha
    class_dict = {'BARBARIAN': [8, 3, 8, 1, 2, 3], 'BARD': [3, 2, 2, 6, 2, 10], 'CLERIC': [3, 3, 4, 3, 9, 3],
                  'DRUID': [4, 4, 3, 2, 10, 2], 'FIGHTER': [7, 6, 4, 2, 2, 4], 'MONK': [6, 7, 5, 1, 1, 5],
                  'PALADIN': [5, 5, 3, 4, 2, 6], 'RANGER': [3, 10, 1, 1, 7, 3], 'ROGUE': [3, 9, 2, 1, 3, 7],
                  'WIZARD': [1, 4, 1, 4, 6, 9], 'MAGE': [1, 3, 2, 10, 4, 5]}
    name_select = str(f"Name = '{name}'")
    result = Cn.select_function('race', name_select)
    cod_r, name_r, race_r, class_r = result[0]
    strength, dexterity, constitution, intelligence, wisdom, charisma = class_dict[class_r]
    message_v = Lang.base_attributes_display(language)
    message = message_v[6]
    print(message.format(race_lang, strength, dexterity, constitution, intelligence, wisdom, charisma))
    Cn.insert_function('character_attr', 'Name', 'Str', 'Dex', 'Cons', 'Intel', 'Wis', 'Cha', Name=f'{name_r}',
                       stra=f'{strength}', dex=f'{dexterity}', consa=f'{constitution}', inta=f'{intelligence}',
                       wisa=f'{wisdom}', chaa=f'{charisma}')
    condition = 'Location = 1'
    where = f"Name = '{name}'"
    Cn.update_function('name', condition, where)
    time.sleep(3)
    return True
