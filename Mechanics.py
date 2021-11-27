import random
import sys
import time
import keyboard as kb
import Connection as Cn
import Dialogues as Dg
import Language
import Language as Lang


def d20():
    """Random number list with 2 numbers from 0 to 20

          Return:\n
          the list with the 2 values
          """
    result_final = []
    list_result = []
    for i in range(30):
        Dg.clear()
        for index in range(2):
            result = random.randint(0, 20)
            list_result.append(result)
            if i == 29:
                result_final.append(result)
        sys.stdout.write('D20: ' + str(list_result[0]) + '   D20: ' + str(list_result[1]))
        sys.stdout.flush()
        list_result.clear()
        time.sleep(0.1)
    return result_final


def d10():
    """Random number with 1 number from 0 to 10

              Return:\n
              the result from random
              """
    result = 0
    for i in range(35):
        Dg.clear()
        result = random.randint(0, 10)
        sys.stdout.write('D10: ' + str(result))
        sys.stdout.flush()
        time.sleep(0.1)
    return result


def d10_luck_number(quantity):
    """list of random numbers with N numbers by quantity argument

                  Return:\n
                  list with numbers arranged in ascending order ranging from 0 to 10 \n
                  Example: if the quantity is 4, will add one more number to quantity and will return [0, 1, 2, 6, 9]
                  """
    quantity += 1
    result = random.sample(range(10), int(quantity))
    result.sort()
    return result


def add_character_status(character_name, debuff, dice, lang, is_in_combat):
    d_type, d_time = debuff
    try:
        # will select the player stats for update new attributes
        where = f"name = '{character_name}'"
        query_stats = Cn.select_function('stats', where)
        cod, name, health_points, attack, defense, debuff_type, debuff_timer = query_stats[0]
        query_attributes = Cn.select_function('character_attr', where)
        cod, name, strength, dexterity, constitution, intelligence, wisdom, charisma = query_attributes[0]
        health_points = int(constitution * 40)
        debuff_lang = Lang.debuff_dictionary()
        debuff_en, debuff_pt_br = debuff_lang[d_type]
        try:
            # if this function called in d20 the dice will be True and will update the debuff timer
            if dice:
                if d_type != debuff_type and d_type > 0:
                    time.sleep(1)
                    condition = f'debuffType = {d_type}, debuffTimer = {d_time}'
                    where = f"Name = '{name}'"
                    Cn.update_function('stats', condition, where)
                elif d_type == debuff_type and d_time > 1:
                    time.sleep(1)
                    condition = f'debuffTimer = {d_time - 1}'
                    where = f"Name = '{name}'"
                    Cn.update_function('stats', condition, where)
                elif debuff_type != 0 and debuff_timer == 1:
                    time.sleep(1)
                    if lang == 0:
                        print(f'\nThe debuff {debuff_en} is over')
                    else:
                        print(f'\nO debuff {debuff_pt_br} acabou')
                    condition = 'debuffType = 0, debuffTimer = 0'
                    where = f"Name = '{name}'"
                    Cn.update_function('stats', condition, where)
                elif debuff_type != 0 and debuff_timer > 1:
                    time.sleep(1)
                    if lang == 0:
                        if debuff_timer - 1 == 1:
                            print(f'\nThe debuff {debuff_en} will be active for one more turn')
                        else:
                            print(f'\nThe debuff {debuff_en} will be active for more {debuff_timer - 1} turns')
                    else:
                        if debuff_timer - 1 == 1:
                            print(f'\nO debuff {debuff_pt_br} estará ativo por mais 1 jogada')
                        else:
                            print(f'\nO debuff {debuff_pt_br} estará ativo por mais {debuff_timer - 1} jogadas')
                    condition = f'debuffTimer = {debuff_timer - 1}'
                    where = f"Name = '{name}'"
                    Cn.update_function('stats', condition, where)
                else:
                    time.sleep(1)
                    condition = f'debuffType = {d_type}, debuffTimer = {d_time}'
                    where = f"Name = '{name}'"
                    Cn.update_function('stats', condition, where)
            query_equipped = Cn.select_function('equiped', where)
            cod, name, armor_name, armor_stat, weapon_name, weapon_stat, weapon_type = query_equipped[0]
            # after search equipped characters equipment if armor is not empty then will sum the armor stat + the
            # character dex attribute, else only the dex attribute of the character
            if armor_stat is not None:
                defense = int(armor_stat * 10) + int(dexterity * 10)
            else:
                defense = int(dexterity * 10)
            # like in armor above will check if weapon is not empty and sum weapon stat + character strength
            if weapon_stat is not None:
                if weapon_type == 'STR':
                    attack = int(weapon_stat * 10) + int(strength * 10)
                elif weapon_type == 'INT':
                    attack = int(weapon_stat * 10) + int(intelligence * 10)
                else:
                    attack = int(weapon_stat * 10) + int(dexterity * 10)
            else:
                attack = int(strength * 10)
            time.sleep(1)
            # if character don't have debuff the debuff_type will be 0 and will update the character health_points,
            # attack and defense
            if debuff_type == 0:
                time.sleep(1)
                condition = f'health_points = {health_points}, attack = {attack}, defense = {defense}'
            else:
                time.sleep(1)
                # if character is in combat will be 1 and will update health_points, attack and defense, else will
                # update too the debuff_type and debuff_timer
                if is_in_combat == 1:
                    condition = f'health_points = {health_points}, attack = {attack}, defense = {defense}'
                else:
                    condition = f'health_points = {health_points}, attack = {attack}, defense = {defense}, ' \
                                f'debuffType = {d_type}, debuffTimer = {d_time}'
            where = f"Name = '{name}'"
            Cn.update_function('stats', condition, where)
            return True
        except IndexError:
            # this except will update character attack, defense and debuff if the query for equipped armor or
            # weapons don't return anything
            attack = int(strength * 10)
            defense = int(dexterity * 10)
            if debuff_type == 0:
                condition = f'health_points = {health_points}, attack = {attack}, defense = {defense}'
            else:
                if is_in_combat == 1:
                    condition = f'health_points = {health_points}, attack = {attack}, defense = {defense}'
                else:
                    condition = f'health_points = {health_points}, attack = {attack}, defense = {defense},' \
                                f' debuffType = {d_type}, debuffTimer = {d_time}'
            where = f"Name = '{name}'"
            Cn.update_function('stats', condition, where)
    except IndexError:
        # if the first query for characters stats don't return anything then it will be created the base stats in
        # database using characters attributes
        where = f"name = '{character_name}'"
        query_attributes = Cn.select_function('character_attr', where)
        cod, name, strength, dexterity, constitution, intelligence, wisdom, charisma = query_attributes[0]
        health_points = int(constitution * 40)
        attack = int(strength * 10)
        defense = int(dexterity * 10)
        Cn.insert_function('stats', 'name', 'health_points', 'attack', 'defense', 'debuffType', 'debuffTimer',
                           name=f'{character_name}', health_points=f'{health_points}', attack=f'{attack}',
                           defense=f'{defense}', debuffType=f'{d_type}', debuffTimer=f'{d_time}')
        return False


def add_item_to_inventory(name, item_name_en, item_attr, item_attr_value, item_name_pt_br, quantity, item_type):
    try:
        # check if the item exists in the characters inventory
        where = str(f"Name = '{name}' AND weaponNameEN = '{item_name_en}'")
        update = Cn.select_function('inventory', where)
        update_result = update[0][3]
        if item_name_en == update_result:
            # update item quantity in inventory
            update_quantity = update[0][7]
            quantity = int(quantity) + int(update_quantity)
            Cn.update_function('inventory', f'quantity = {quantity}', where)
    except IndexError:
        try:
            # will select the last Slot Index from characters inventory and will add 1 to index and will insert the
            # item in database
            name_select = str(f"Name = '{name}'")
            result = Cn.select_index_inventory('inventory', name_select, 'SlotIndex')
            index = result[0][0] + 1
            Cn.insert_function('inventory', 'Name', 'SlotIndex', 'weaponNameEN', 'weaponAttrType', 'weaponAttrValue',
                               'weaponNamePT_BR', 'quantity', 'item_type', Name=f'{name}', SlotIndex=f'{index}',
                               weaponNameEN=f'{item_name_en}',
                               weaponAttrType=f'{item_attr}', weaponAttrValue=f'{item_attr_value}',
                               weaponNamePT_BR=f'{item_name_pt_br}', quantity=f'{quantity}', item_type=f'{item_type}')
        except TypeError:
            # if the result from select Slot index from above don't return anything, then characters don't have any
            # itens on inventory, then will be add the item in slot index 0
            Cn.insert_function('inventory', 'Name', 'SlotIndex', 'weaponNameEN', 'weaponAttrType', 'weaponAttrValue',
                               'weaponNamePT_BR', 'quantity', 'item_type', Name=f'{name}', SlotIndex='0',
                               weaponNameEN=f'{item_name_en}',
                               weaponAttrType=f'{item_attr}', weaponAttrValue=f'{item_attr_value}',
                               weaponNamePT_BR=f'{item_name_pt_br}', quantity=f'{quantity}', item_type=f'{item_type}')


def add_skill_to_character(name, skill_name, skill_level):
    try:
        # will search for the characters name, skill name and will update the skill level
        name_select = str(f"Name = '{name}' AND skillName = '{skill_name}'")
        result = Cn.select_function('skill', name_select)
        cod, char_name, skill, skill_lvl = result[0]
        if skill == skill_name:
            skill_to_update = float(skill_lvl) + float(skill_level)
            Cn.update_function('skill', f'skillLevel = {skill_to_update}', name_select)
    except IndexError:
        # if the skill name in character is not found, then will be inserted
        Cn.insert_function('skill', 'name', 'skillName', 'skillLevel', name=f'{name}', skillName=f'{skill_name}',
                           skillLevel=f'{skill_level}')


def skill_test(name, start_dialogue, success_crit, success, failure, failure_crit, result_text, after_success, found,
               not_found, luck_number, base_attr, character_class, skill_name, item_quantity_to_add, d20_test_pass,
               item_lang_location, item_type, debuff, lang):
    # will display the first dialogue before start the skill test
    sys.stdout.write(start_dialogue)
    attributes = Cn.select_function('character_attr', f"Name = '{name}'")
    base = attributes[0][base_attr]
    item_name_en, item_attr, item_attr_value, item_name_pt_br = item_lang_location()[character_class]
    result = d20()
    value1, value2 = result
    sum_d20 = int(value1) + int(value2) + int(base)
    print(result_text.format(value1, value2, base, sum_d20))
    # will get the characters attributes, item attributes character may retrieve if critical success or success in
    # skill test, will play the d20 and sum the result of the first d20 + second d20 + character base attribute and
    # display the result for player
    while True:
        if kb.is_pressed('space'):
            Dg.clear()
            break
    if sum_d20 > d20_test_pass[3]:
        # Critical success
        time.sleep(0.05)
        sys.stdout.write(success_crit)
        debuff_none = [0, 0]
        add_character_status(name, debuff_none, True, lang, 0)
        add_skill_to_character(name, skill_name, '1')
        sys.stdout.write(after_success)
        add_item_to_inventory(name, item_name_en, item_attr, item_attr_value, item_name_pt_br,
                              item_quantity_to_add, item_type)
        # will update/add character status, update/add skill to the character, and update/add item to the
        # character inventory
        while True:
            if kb.is_pressed('space'):
                Dg.clear()
                break
        sys.stdout.write(found)
        return True
    elif d20_test_pass[2] < sum_d20 <= d20_test_pass[3]:
        # Success
        time.sleep(0.05)
        sys.stdout.write(success)
        debuff_none = [0, 0]
        add_character_status(name, debuff_none, True, lang, 0)
        add_skill_to_character(name, skill_name, '0.5')
        sys.stdout.write(after_success)
        # will update/add character status, update/add skill to the character
        while True:
            if kb.is_pressed('space'):
                Dg.clear()
                break
        Dg.clear()
        while True:
            skill_query = Cn.select_function('skill', f"Name = '{name}' AND skillName = '{skill_name}'")
            skill_level = skill_query[0][3]
            input_number = d10_luck_number(skill_level)
            item_found = d10()
            print(luck_number.format(input_number))
            # will get the player skill level and will call the function d10_luck_number(quantity), the quantity will be
            # the character skill level, then will call the function d10 and get the random number from 0 to 10
            if item_found in input_number:
                # if result of d10 is found in the list of d10_luck_lumber then player found the item
                sys.stdout.write(found)
                add_item_to_inventory(name, item_name_en, item_attr, item_attr_value, item_name_pt_br,
                                      item_quantity_to_add, 1)
                while True:
                    if kb.is_pressed('space'):
                        Dg.clear()
                        break
                return True
            else:
                # player don't find the item
                sys.stdout.write(not_found)
                while True:
                    if kb.is_pressed('space'):
                        Dg.clear()
                        break
                return True
    elif d20_test_pass[1] < sum_d20 <= d20_test_pass[2]:
        # failure
        time.sleep(0.05)
        sys.stdout.write(failure)
        debuff_none = [0, 0]
        add_character_status(name, debuff_none, True, lang, 0)
        while True:
            if kb.is_pressed('space'):
                Dg.clear()
                return False
    elif d20_test_pass[0] < sum_d20 <= d20_test_pass[1]:
        # critical failure
        time.sleep(0.05)
        sys.stdout.write(failure_crit)
        add_character_status(name, debuff, True, lang, 0)
        # will be add a debuff to character
        while True:
            if kb.is_pressed('space'):
                Dg.clear()
                return False


def prepare_for_skill_test(character_name, skill_name, language, class_text, d20_pass, skill_test_dialogue,
                           item_quantity_reward, character_base_attribute, item_lang_location, query, item_type,
                           debuff):
    # load skill dictionary, skil name english and portuguese
    skill_dictionary = Lang.skills_dictionary()
    skill_en, skill_pt_br = skill_dictionary[skill_name]
    try:
        # get skill level and name for use in d10 function with character get success in dices
        skill_query = Cn.select_function('skill', f"Name = '{character_name}' AND skillName = '{skill_en}'")
        skill_level = skill_query[0][3]
        skill_name = skill_query[0][2]
        start_dialogue, success_crit, success, failure, failure_crit, result_text, after_success, found, not_found, \
        luck_number = skill_test_dialogue(language, class_text, skill_level, skill_name, skill_pt_br,
                                          character_base_attribute, query)
    except IndexError:
        # if don't return anything from skill level and name then in d10 function the skill level will be 0
        start_dialogue, success_crit, success, failure, failure_crit, result_text, after_success, found, not_found, \
        luck_number = skill_test_dialogue(language, class_text, 0, skill_en, skill_pt_br, character_base_attribute,
                                          query)
    # skill test function will be called with the arguments
    skill_test(character_name, start_dialogue, success_crit, success, failure, failure_crit, result_text, after_success,
               found, not_found, luck_number, character_base_attribute, class_text, skill_en, item_quantity_reward,
               d20_pass, item_lang_location, item_type, debuff, language)


def query_equip_item(character_name, item_name, item_name_en, item_type, item_stat,
                     item_attribute_value, item_attribute_type, item_quantity, lang, item_index):
    # IF ITEM TYPE 1 THEN IS WEAPON
    condition = ''
    if item_name is not None:
        # CHECK IF THERE IS AN WEAPON EQUIPED
        if item_name == item_name_en:
            pass
        else:
            translation_name = Lang.all_items()
            for key in translation_name:
                if item_name in key:
                    # ADD THE EQUIPPED WEAPON BACK TO INVENTORY
                    name_pt_br = translation_name[key][2]
                    if item_index == 1:
                        add_item_to_inventory(character_name, item_name, item_type, item_stat,
                                              name_pt_br, 1, 1)
                    elif item_index == 2:
                        add_item_to_inventory(character_name, item_name, item_type, item_stat,
                                              name_pt_br, 1, 2)
            # ADD THE WEAPON CHOOSE FROM PLAYER INVENTORY TO EQUIPPED
            if item_index == 1:
                condition = f"weapon_name = '{item_name_en}', weapon_stat = '{item_attribute_value}'" \
                            f", weapon_type =  '{item_attribute_type}'"
            elif item_index == 2:
                condition = f"armor_name = '{item_name_en}', armor_stat = '{item_attribute_value}'"
            where = f"Name = '{character_name}'"
            Cn.update_function('equiped', condition, where)
            # AFTER INSERT THE WEAPON IN EQUIPPED, THIS FUNCTION CHECKS IF THE WEAPON CHOOSE
            # HAS ONLY 1 IN INVENTORY
            if item_quantity == 1:
                # IF TRUE, THEN DELETE THE WEAPON FROM INVENTORY AND REORGANIZE
                # SLOT INDEX OF ALL ITEMS
                where = f"name = '{character_name}' AND weaponNameEN = '{item_name_en}'"
                Cn.delete_function('inventory', where)
                where = f"name = '{character_name}'"
                query_inventory = Cn.select_function('inventory', where)
                for cod, name, slot_index, item_name_en, item_attribute_type, \
                    item_attribute_value, item_name_pt_br, item_quantity, \
                        item_index in query_inventory:
                    if slot_index == 0:
                        pass
                    else:
                        condition = f'SlotIndex = {slot_index - 1}'
                        where = f"Name = '{character_name}'"
                        Cn.update_function('inventory', condition, where)
            else:
                # IF FALSE THEN PLAYER HAVE MORE THAN ONE OF SAME WEAPON, ONLY
                # SUBTRACT ONE FROM QUANTITY
                condition = f'quantity = {item_quantity - 1}'
                where = f"Name = '{character_name}' AND weaponNameEN = '{item_name_en}'"
                Cn.update_function('inventory', condition, where)
        equip_item(character_name, lang)
    else:
        # IF THE PLAYER IS NOT EQUIPPING ANY WEAPONS, THEN EQUIP FROM INVENTORY
        if item_index == 1:
            condition = f"weapon_name = {item_name_en}, weapon_stat = {item_attribute_value}" \
                        f", weapon_type =  {item_attribute_type}"
        elif item_index == 2:
            condition = f"armor_name = {item_name_en}, armor_stat = {item_attribute_value}"
        where = f"Name = '{character_name}'"
        Cn.update_function('equiped', condition, where)
        where = f"name = '{character_name}' AND weaponNameEN = '{item_name_en}'"
        query_inventory = Cn.select_function('inventory', where)
        cod, name, slot_index, item_name_en, item_attribute_type, item_attribute_value, \
            item_name_pt_br, item_quantity, item_index = query_inventory[0]
        if item_quantity == 1:
            # IF THE WEAPON EQUIPPED HAS ONLY ONE ON INVENTORY THEN DELETE AND
            # REORGANIZE THE SLOT INDEX
            where = f"name = '{character_name}' AND weaponNameEN = '{item_name_en}'"
            Cn.delete_function('inventory', where)
            where = f"name = '{character_name}'"
            query_inventory = Cn.select_function('inventory', where)
            for cod, name, slot_index, item_name_en, item_attribute_type, \
                item_attribute_value, item_name_pt_br, item_quantity, \
                    item_index in query_inventory:
                if slot_index == 0:
                    pass
                else:
                    # IF SLOT INDEX > 0 THEN PLAYER HAS MORE ITEMS, SUBTRACT
                    # ONE FOR EACH SLOT INDEX
                    condition = f'SlotIndex = {slot_index - 1}'
                    where = f"Name = '{character_name}'"
                    Cn.update_function('inventory', condition, where)
                equip_item(character_name, lang)
        else:
            # PLAYER HAS MORE THEN ONE WEAPON, THEN ONLY NEED TO SUBTRACT ONE FROM QUANTITY
            condition = f'quantity = {item_quantity - 1}'
            where = f"Name = '{character_name}' AND weaponNameEN = '{item_name_en}'"
            Cn.update_function('equiped', condition, where)
        equip_item(character_name, lang)


def equip_item(character_name, lang):
    Dg.clear()
    inventory_text, slot_text, quantity_text, name_text, exit_text, choose_text, empty = Language.inventory_language(
        lang)
    sys.stdout.write(inventory_text)
    close_inventory = 0
    where_character = f"name = '{character_name}'"
    try:
        query_inventory = Cn.select_function('inventory', where_character)
        for cod, name, slot_index, weapon_name_en, weapon_attribute_type, weapon_attribute_value, weapon_name_pt_br, \
            quantity, item_type in query_inventory:
            if lang == 0:
                string = (slot_text + str(slot_index) + quantity_text + str(quantity) + '   ' + str(
                    weapon_attribute_type)
                          + ':' + str(weapon_attribute_value) + name_text + str(weapon_name_en))
                sys.stdout.write(string + '\n')
            else:
                string = (slot_text + str(slot_index) + quantity_text + str(quantity) + '   ' + str(
                    weapon_attribute_type) + ':' +
                          str(weapon_attribute_value) + name_text + str(weapon_name_pt_br))
                sys.stdout.write(string + '\n')

        if len(query_inventory) == 1:
            exit_option = 1
        else:
            exit_option = len(query_inventory)
        sys.stdout.write(exit_text.format(exit_option))
        sys.stdout.flush()
        while close_inventory < 1:
            option = input(choose_text)
            if int(option) == int(exit_option):
                debuff = [0, 0]
                add_character_status(character_name, debuff, False, lang, 0)
                return True
            elif int(exit_option) > int(option) >= 0:
                close_inventory = 2
                # SELECT OPTION BY THE ITEM INDEX
                where = f"name = '{character_name}' AND SlotIndex = '{int(option)}'"
                query_inventory = Cn.select_function('inventory', where)
                cod, name, slot_index, weapon_name_en, weapon_attribute_type, weapon_attribute_value, \
                weapon_name_pt_br, quantity, item_type = query_inventory[0]
                if item_type == 0:
                    # ITEM TYPE 0 IS POTION
                    pass
                else:
                    try:
                        # QUERY FOR ITENS EQUIPED
                        query_equiped = Cn.select_function('equiped', where_character)
                        cod, name, armor_name, armor_stat, weapon_name, weapon_stat, weapon_type = query_equiped[0]
                        query_equip_item(character_name, weapon_name, weapon_name_en, weapon_type, weapon_stat,
                                         weapon_attribute_value, weapon_attribute_type, quantity, lang, item_type)
                    except IndexError:
                        # DONT FIND ANY EQUIPED ITEMS IN CHARACTER
                        if item_type == 1:
                            # ITEM TYPE = 1 THEN THE NEW EQUIPED ITEM IS AN WEAPON, INSERT IN EQUIPED TABLE
                            Cn.insert_function('equiped', 'name', 'weapon_name', 'weapon_stat', 'weapon_type',
                                               name=f'{character_name}',
                                               weapon_name=f'{weapon_name_en}', weapon_stat=f'{weapon_attribute_value}',
                                               weapon_type=f'{weapon_attribute_type}')
                            where_ch_weap_name = f"name = '{character_name}' AND weaponNameEN = '{weapon_name_en}'"
                            query_inventory = Cn.select_function('inventory', where_ch_weap_name)
                            cod, name, slot_index, weapon_name_en, weapon_attribute_type, weapon_attribute_value, \
                            weapon_name_pt_br, quantity, item_type = query_inventory[0]
                            if quantity == 1:
                                # IF THE ITEM QUANTITY IN INVENTORY IS ONE, NEED TO DELETE FROM INVENTORY AND
                                # REORGANIZE SLOTINDEX
                                Cn.delete_function('inventory', where_ch_weap_name)
                            else:
                                # PLAYER HAS MORE THAN ONE FROM SAME WEAPON, ONE NEED TO SUBTRACT ONE FROM QUANTITY
                                condition = f'quantity = {quantity - 1}'
                                Cn.update_function('inventory', condition, where_ch_weap_name)
                            equip_item(character_name, lang)
                        elif item_type == 2:
                            Cn.insert_function('equiped', 'name', 'armor_name', 'armor_stat',
                                               name=f'{character_name}',
                                               armor_name=f'{weapon_name_en}', armor_stat=f'{weapon_attribute_value}')
                            equip_item(character_name, lang)
                        return True
        close_inventory = 2
    except IndexError:
        # DONT HAVE ITENS IN INVENTORY TO LIST
        sys.stdout.write(empty)
        sys.stdout.flush()


def calc_attack(debuff_type, enemy_life, damage, d20_result, character_name, lang, debuff_timer, enemy_attack):
    crit_success_lang, crit_lang, failure_lang, dead_text_lang, hit_text_lang, active_debuff, enemy_dead_lang, enemy_hit_lang, missed_hit_lang = Language.calc_attack_language(
        lang)
    if d20_result == 4:
        Dg.clear()
        print(crit_success_lang)
    elif d20_result == 3:
        Dg.clear()
        print(crit_lang)
    elif d20_result == 2:
        Dg.clear()
        print(failure_lang)
    while True:
        if kb.is_pressed('space'):
            break
    if enemy_attack >= 1:
        Dg.clear()
        try:
            where = f"name = '{character_name}'"
            query_stats = Cn.select_function('stats', where)
            cod, name, health_points, attack, defense, debuff_type, debuff_timer = query_stats[0]
            condition = f'health_points = {health_points - damage}'
            where = f"Name = '{character_name}'"
            Cn.update_function('stats', condition, where)
            if health_points - damage <= 0:
                print(dead_text_lang.format(int(damage)))
            else:
                print(hit_text_lang.format(int(damage), int(health_points - damage)))
            time.sleep(2)
            while True:
                if kb.is_pressed('space'):
                    return health_points - damage
        except IndexError:
            pass
    else:
        if debuff_type > 0:
            debuff = [debuff_type, debuff_timer]
            Dg.clear()
            print(active_debuff)
            add_character_status(character_name, debuff, True, lang, 1)
            time.sleep(2)
            while True:
                if kb.is_pressed('space'):
                    break
            result_d10 = d10()
            if result_d10 > 5:
                enemy_life -= int(damage)
                Dg.clear()
                if enemy_life <= 0:
                    print(enemy_dead_lang.format(int(damage)))
                else:
                    print(enemy_hit_lang.format(int(damage), int(enemy_life)))
                time.sleep(2)
                while True:
                    if kb.is_pressed('space'):
                        return enemy_life
            else:
                Dg.clear()
                print(missed_hit_lang)
                time.sleep(2)
                while True:
                    if kb.is_pressed('space'):
                        return enemy_life
        else:
            enemy_life -= int(damage)
            if enemy_life <= 0:
                print(enemy_dead_lang.format(int(damage)))
            else:
                print(enemy_hit_lang.format(int(damage), int(enemy_life)))
            time.sleep(2)
            while True:
                if kb.is_pressed('space'):
                    return enemy_life


def attack_system(character_name, enemy_name, enemy_life, lang, d20_test_pass):
    attack_text, missed_attack = Language.attack_system_language(lang)
    sys.stdout.write('\n' + attack_text.format(enemy_name))
    while True:
        if kb.is_pressed('space'):
            break
    result = d20()
    value1, value2 = result
    sum_d20 = value1 + value2
    try:
        where = f"name = '{character_name}'"
        query_stats = Cn.select_function('stats', where)
        cod, name, health_points, attack, defense, debuff_type, debuff_timer = query_stats[0]
        if sum_d20 > d20_test_pass[3]:
            best_d20 = sum_d20 + attack
            enemy_hit = calc_attack(debuff_type, enemy_life, best_d20, 4, character_name, lang, debuff_timer, 0)
            return enemy_hit
        elif d20_test_pass[2] < sum_d20 <= d20_test_pass[3]:
            if value1 > value2:
                best_d20 = value1 + attack
            else:
                best_d20 = value2 + attack
            enemy_hit = calc_attack(debuff_type, enemy_life, best_d20, 3, character_name, lang, debuff_timer, 0)
            return enemy_hit
        elif d20_test_pass[1] < sum_d20 <= d20_test_pass[2]:
            enemy_hit = calc_attack(debuff_type, enemy_life, attack - (attack * .1), 2, character_name, lang,
                                    debuff_timer, 0)
            return enemy_hit
        elif d20_test_pass[0] < sum_d20 <= d20_test_pass[1]:
            print('\n' + missed_attack)
            while True:
                if kb.is_pressed('space'):
                    break
            return enemy_life
    except IndexError:
        pass


def enemy_attack(character_name, enemy_name, lang, d20_test_pass, hit, defense_hit):
    attack_text, display_hit_calc, enemy_missed_hit = Language.enemy_attack_language(lang)
    print(attack_text.format(enemy_name))
    while True:
        if kb.is_pressed('space'):
            break
    result = d20()
    value1, value2 = result
    sum_d20 = value1 + value2
    try:
        where = f"name = '{character_name}'"
        query_stats = Cn.select_function('stats', where)
        cod, name, health_points, attack, defense, debuff_type, debuff_timer = query_stats[0]
        if sum_d20 > d20_test_pass[3]:
            best_d20 = sum_d20 + hit
            print('\n' + display_hit_calc.format(enemy_name, best_d20, defense_hit, best_d20 - defense_hit))
            time.sleep(3)
            if (best_d20 - defense_hit) <= 0:
                player_life = calc_attack(debuff_type, health_points, 0, 4, character_name, lang, debuff_timer, 1)
            else:
                player_life = calc_attack(debuff_type, health_points, best_d20, 4, character_name, lang, debuff_timer,
                                          1)
            return player_life
        elif d20_test_pass[2] < sum_d20 <= d20_test_pass[3]:
            if value1 > value2:
                best_d20 = value1 + hit
            else:
                best_d20 = value2 + hit
            print('\n' + display_hit_calc.format(enemy_name, best_d20, defense_hit, best_d20 - defense_hit))
            time.sleep(3)
            if best_d20 - defense_hit <= 0:
                player_life = calc_attack(debuff_type, health_points, 0, 3, character_name, lang, debuff_timer, 1)
            else:
                player_life = calc_attack(debuff_type, health_points, best_d20, 3, character_name, lang, debuff_timer,
                                          1)
            return player_life
        elif d20_test_pass[1] < sum_d20 <= d20_test_pass[2]:
            print('\n' + display_hit_calc.format(enemy_name, (hit - (hit * 0.1)), defense_hit, (hit - (hit * 0.1)) -
                                                 defense_hit))
            time.sleep(3)
            if (hit - (hit * 0.1)) - defense_hit <= 0:
                player_life = calc_attack(debuff_type, health_points, 0, 2, character_name, lang, debuff_timer, 1)
            else:
                player_life = calc_attack(debuff_type, health_points, hit - (hit * .1), 2, character_name, lang,
                                          debuff_timer, 1)
            return player_life
        elif d20_test_pass[0] < sum_d20 <= d20_test_pass[1]:
            print('\n' + enemy_missed_hit.format(enemy_name))
            time.sleep(3)
            return 1
    except IndexError:
        pass


def defense_system(character_name, enemy_name, lang, d20_test_pass):
    try_defense_attack, crit_success_lang, crit_lang, failure_lang, \
    crit_failure_lang = Language.defense_system_language(lang)
    sys.stdout.write('\n' + try_defense_attack.format(enemy_name))
    while True:
        if kb.is_pressed('space'):
            break
    result = d20()
    value1, value2 = result
    sum_d20 = value1 + value2
    try:
        where = f"name = '{character_name}'"
        query_stats = Cn.select_function('stats', where)
        cod, name, health_points, attack, defense, debuff_type, debuff_timer = query_stats[0]
        if sum_d20 > d20_test_pass[3]:
            best_d20 = sum_d20 + defense
            print('\n' + crit_success_lang.format(best_d20))
            while True:
                if kb.is_pressed('space'):
                    return best_d20
        elif d20_test_pass[2] < sum_d20 <= d20_test_pass[3]:
            if value1 > value2:
                best_d20 = value1 + defense
            else:
                best_d20 = value2 + defense
            print('\n' + crit_lang.format(best_d20))
            while True:
                if kb.is_pressed('space'):
                    return best_d20
        elif d20_test_pass[1] < sum_d20 <= d20_test_pass[2]:
            print('\n' + failure_lang.format(defense))
            while True:
                if kb.is_pressed('space'):
                    return defense
        elif d20_test_pass[0] < sum_d20 <= d20_test_pass[1]:
            print('\n' + crit_failure_lang)
            return 0
        while True:
            if kb.is_pressed('space'):
                break
    except IndexError:
        pass


def combat(character_name, enemy_name, enemy_life, lang, d20_test_pass, hit):
    start_text, reaction_text, dead_text = Language.combat_language(lang)
    sys.stdout.write(start_text)
    while True:
        if kb.is_pressed('0'):
            Dg.clear()
            enemy_life = attack_system(character_name, enemy_name, enemy_life, lang, d20_test_pass)
            if enemy_life > 0:
                print(reaction_text)
                time.sleep(1)
                if kb.is_pressed('space'):
                    break
                player_life = enemy_attack(character_name, enemy_name, lang, d20_test_pass, hit, 0)
                if player_life <= 0:
                    print(dead_text)
                    exit()
                elif enemy_life <= 0:
                    exit()
                time.sleep(1)
                if kb.is_pressed('space'):
                    break
                Dg.clear()
                sys.stdout.write(start_text)
        elif kb.is_pressed('1'):
            Dg.clear()
            character_defense = defense_system(character_name, enemy_name, lang, d20_test_pass)
            player_life = enemy_attack(character_name, enemy_name, lang, d20_test_pass, hit, character_defense)
            if player_life <= 0:
                print(dead_text)
                exit()
            elif enemy_life <= 0:
                exit()
            time.sleep(1)
            if kb.is_pressed('space'):
                break
            Dg.clear()
            sys.stdout.write(start_text)
        elif kb.is_pressed('2'):
            inventory = equip_item(character_name, lang)
            if inventory:
                Dg.clear()
                time.sleep(1)
                sys.stdout.write(start_text)