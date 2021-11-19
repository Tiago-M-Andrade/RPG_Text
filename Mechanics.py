import random
import time
import sys
import Dialogues as Dg
import Connection as Cn
import keyboard as kb
import Language as Lang


def d20():
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
    result = 0
    for i in range(35):
        Dg.clear()
        result = random.randint(0, 10)
        sys.stdout.write('D10: ' + str(result))
        sys.stdout.flush()
        time.sleep(0.1)
    return result


def d10LuckNumber(quantity):
    quantity += 1
    result = random.sample(range(10), int(quantity))
    result.sort()
    return result


def add_item_to_inventory(name, weapon_name_en, weapon_attr, weapon_attr_value, weapon_name_pt_br, quantity, item_type):
    try:
        name_select = str(f"Name = '{name}'")
        where = str(f"Name = '{name}' AND weaponNameEN = '{weapon_name_en}'")
        update = Cn.select_function('inventory', where)
        update_result = update[0][3]
        if weapon_name_en == update_result:
            update_quantity = update[0][7]
            quantity = int(quantity) + int(update_quantity)
            Cn.update_function('inventory', f'quantity = {quantity}', where)
    except IndexError:
        try:
            name_select = str(f"Name = '{name}'")
            result = Cn.select_index_inventory('inventory', name_select, 'SlotIndex')
            index = result[0][0] + 1
            Cn.insert_function('inventory', 'Name', 'SlotIndex', 'weaponNameEN', 'weaponAttrType', 'weaponAttrValue',
                               'weaponNamePT_BR', 'quantity', 'item_type', Name=f'{name}', SlotIndex=f'{index}',
                               weaponNameEN=f'{weapon_name_en}',
                               weaponAttrType=f'{weapon_attr}', weaponAttrValue=f'{weapon_attr_value}',
                               weaponNamePT_BR=f'{weapon_name_pt_br}', quantity=f'{quantity}', item_type=f'{item_type}')
        except TypeError:
            Cn.insert_function('inventory', 'Name', 'SlotIndex', 'weaponNameEN', 'weaponAttrType', 'weaponAttrValue',
                               'weaponNamePT_BR', 'quantity', 'item_type', Name=f'{name}', SlotIndex='0',
                               weaponNameEN=f'{weapon_name_en}',
                               weaponAttrType=f'{weapon_attr}', weaponAttrValue=f'{weapon_attr_value}',
                               weaponNamePT_BR=f'{weapon_name_pt_br}', quantity=f'{quantity}', item_type=f'{item_type}')


def add_skill_to_character(name, skill_name, skill_level):
    try:
        name_select = str(f"Name = '{name}' AND skillName = '{skill_name}'")
        result = Cn.select_function('skill', name_select)
        cod, char_name, skill, skill_lvl = result[0]
        if skill == skill_name:
            skill_to_update = float(skill_lvl) + float(skill_level)
            Cn.update_function('skill', f'skillLevel = {skill_to_update}', name_select)
    except IndexError:
        Cn.insert_function('skill', 'name', 'skillName', 'skillLevel', name=f'{name}', skillName=f'{skill_name}',
                           skillLevel=f'{skill_level}')


def skill_test(name, start_dialogue, success_crit, success, failure, failure_crit, result_text, after_success, found,
               not_found, luck_number, base_attr, character_class, skill_name, item_quantity_to_add, d20_test_pass,
               item_lang_location):
    sys.stdout.write(start_dialogue)
    attributes = Cn.select_function('character_attr', f"Name = '{name}'")
    base = attributes[0][base_attr]
    weapon_name_en, weapon_attr, weapon_attr_value, weapon_name_pt_br = item_lang_location()[character_class]
    result = d20()
    value1, value2 = result
    sum_d20 = int(value1) + int(value2) + int(base)
    print(result_text.format(value1, value2, base, sum_d20))
    # sum_d20 = 36
    while True:
        if kb.is_pressed('space'):
            Dg.clear()
            break
    if sum_d20 > d20_test_pass[3]:
        time.sleep(0.05)
        sys.stdout.write(success_crit)
        add_skill_to_character(name, skill_name, '1')
        sys.stdout.write(after_success)
        add_item_to_inventory(name, weapon_name_en, weapon_attr, weapon_attr_value, weapon_name_pt_br,
                              item_quantity_to_add)
        while True:
            if kb.is_pressed('space'):
                Dg.clear()
                break
        sys.stdout.write(found)
        return True
    elif d20_test_pass[2] < sum_d20 <= d20_test_pass[3]:
        time.sleep(0.05)
        sys.stdout.write(success)
        add_skill_to_character(name, skill_name, '0.5')
        sys.stdout.write(after_success)
        while True:
            if kb.is_pressed('space'):
                Dg.clear()
                break
        Dg.clear()
        while True:
            skill_query = Cn.select_function('skill', f"Name = '{name}' AND skillName = '{skill_name}'")
            skill_level = skill_query[0][3]
            input_number = d10LuckNumber(skill_level)
            weaponfound = d10()
            print(luck_number.format(input_number))
            if weaponfound in input_number:
                sys.stdout.write(found)
                add_item_to_inventory(name, weapon_name_en, weapon_attr, weapon_attr_value, weapon_name_pt_br, 1)
                while True:
                    if kb.is_pressed('space'):
                        Dg.clear()
                        break
                return True
            else:
                sys.stdout.write(not_found)
                while True:
                    if kb.is_pressed('space'):
                        Dg.clear()
                        break
                return True
    elif d20_test_pass[1] < sum_d20 <= d20_test_pass[2]:
        time.sleep(0.05)
        sys.stdout.write(failure)
        while True:
            if kb.is_pressed('space'):
                Dg.clear()
                return False
    elif d20_test_pass[0] < sum_d20 <= d20_test_pass[1]:
        time.sleep(0.05)
        sys.stdout.write(failure_crit)
        while True:
            if kb.is_pressed('space'):
                Dg.clear()
                return False
    # sys.stdout.flush()


def prepare_for_skill_test(character_name, skill_name, language, class_text, d20_pass, skill_test_dialogue,
                           item_quantity_reward, character_base_attribute, item_lang_location, query):
    skill_dictionary = Lang.skills_dictionary()
    skill_en, skill_pt_br = skill_dictionary[skill_name]
    try:
        skill_query = Cn.select_function('skill', f"Name = '{character_name}' AND skillName = '{skill_en}'")
        skill_level = skill_query[0][3]
        skill_name = skill_query[0][2]
        start_dialogue, success_crit, success, failure, failure_crit, result_text, after_success, found, not_found, \
        luck_number = skill_test_dialogue(language, class_text, skill_level, skill_name, skill_pt_br,
                                          character_base_attribute, query)
    except IndexError:
        start_dialogue, success_crit, success, failure, failure_crit, result_text, after_success, found, not_found, \
        luck_number = skill_test_dialogue(language, class_text, 0, skill_en, skill_pt_br, character_base_attribute,
                                          query)
    skill_test(character_name, start_dialogue, success_crit, success, failure, failure_crit, result_text, after_success,
               found, not_found, luck_number, character_base_attribute, class_text, skill_en, item_quantity_reward,
               d20_pass, item_lang_location)


def combat(character_name, enemy_name):
    sys.stdout.write('O que deseja fazer? \n [0 - ATACAR]   [1 - DEFENDER]  [2 - INVENTÁRIO]')


# print(combat('egilhard', 'lovecraft'))

def add_character_status(character_name, debuff):
    d_type, d_time = debuff
    try:
        where = f"name = '{character_name}'"
        query_stats = Cn.select_function('stats', where)
        cod, name, health_points, attack, defense, debuff_type, debuff_timer = query_stats[0]
        query_attributes = Cn.select_function('character_attr', where)
        cod, name, strength, dexterity, constitution, intelligence, wisdom, charisma = query_attributes[0]
        health_points = int(constitution * 40)
        try:
            query_equiped = Cn.select_function('equiped', where)
            cod, name, armor_name, armor_stat, weapon_name, weapon_stat, weapon_type = query_equiped[0]
            if armor_stat is not None:
                defense = int(armor_stat * 10) + int(dexterity * 10)
            else:
                defense = int(dexterity * 10)
            if weapon_stat is not None:
                if weapon_type == 'STR':
                    attack = int(weapon_stat * 10) + int(strength * 10)
                elif weapon_type == 'INT':
                    attack = int(weapon_stat * 10) + int(intelligence * 10)
                else:
                    attack = int(weapon_stat * 10) + int(dexterity * 10)
            else:
                attack = int(strength * 10)
            condition = f'health_points = {health_points}, attack = {attack}, defense = {defense}, debuff_type = {d_type}, debuff_timer = {d_time}'
            where = f"Name = '{name}'"
            Cn.update_function('stats', condition, where)
        except IndexError:
            attack = int(strength * 10)
            defense = int(dexterity * 10)
            condition = f'health_points = {health_points}, attack = {attack}, defense = {defense}, debuffType = {d_type}, debuffTimer = {d_time}'
            where = f"Name = '{name}'"
            Cn.update_function('stats', condition, where)
    except IndexError:
        where = f"name = '{character_name}'"
        query_attributes = Cn.select_function('character_attr', where)
        cod, name, strength, dexterity, constitution, intelligence, wisdom, charisma = query_attributes[0]
        health_points = int(constitution * 40)
        attack = int(strength * 10)
        defense = int(dexterity * 10)
        Cn.insert_function('stats', 'name', 'health_points', 'attack', 'defense', 'debuffType', 'debuffTimer',
                           name=f'{character_name}', health_points=f'{health_points}', attack=f'{attack}',
                           defense=f'{defense}', debuffType=f'{d_type}', debuffTimer=f'{d_time}')


# debuff = [0, 0]
# print(add_character_status('egilhard', debuff))

def query_equip_itens(character_name, weapon_name, weapon_name_en, weapon_type, weapon_stat,
                      weapon_attribute_value, weapon_attribute_type, quantity, lang, item_type):
    # IF ITEM TYPE 1 THEN IS WEAPON
    condition = ''
    if weapon_name is not None:
        # CHECK IF THERE IS AN WEAPON EQUIPED
        if weapon_name == weapon_name_en:
            pass
        else:
            translation_name = Lang.all_items()
            for key in translation_name:
                if weapon_name in key:
                    # ADD THE EQUIPED WEAPON BACK TO INVENTORY
                    name_pt_br = translation_name[key][2]
                    if item_type == 1:
                        add_item_to_inventory(character_name, weapon_name, weapon_type, weapon_stat,
                                              name_pt_br, 1, 1)
                    elif item_type == 2:
                        add_item_to_inventory(character_name, weapon_name, weapon_type, weapon_stat,
                                              name_pt_br, 1, 2)
            # ADD THE WEAPON CHOOSE FROM PLAYER INVENTORY TO EQUIPED
            if item_type == 1:
                condition = f"weapon_name = '{weapon_name_en}', weapon_stat = '{weapon_attribute_value}'" \
                            f", weapon_type =  '{weapon_attribute_type}'"
            elif item_type == 2:
                condition = f"armor_name = '{weapon_name_en}', armor_stat = '{weapon_attribute_value}'"
            where = f"Name = '{character_name}'"
            Cn.update_function('equiped', condition, where)
            # AFTER INSERT THE WEAPON IN EQUIPED, THIS FUNCTION CHECKS IF THE WEAPON CHOOSE
            # HAS ONLY 1 IN INVENTORY
            if quantity == 1:
                # IF TRUE, THEN DELETE THE WEAPON FROM INVENTORY AND REORGANIZE
                # SLOTINDEX OF ALL ITENS
                where = f"name = '{character_name}' AND weaponNameEN = '{weapon_name_en}'"
                Cn.delete_function('inventory', where)
                where = f"name = '{character_name}'"
                query_inventory = Cn.select_function('inventory', where)
                for cod, name, slot_index, weapon_name_en, weapon_attribute_type, \
                    weapon_attribute_value, weapon_name_pt_br, quantity, \
                        item_type in query_inventory:
                    if slot_index == 0:
                        pass
                    else:
                        condition = f'SlotIndex = {slot_index - 1}'
                        where = f"Name = '{character_name}'"
                        Cn.update_function('inventory', condition, where)
            else:
                # IF FALSE THEN PLAYER HAVE MORE THAN ONE OF SAME WEAPON, ONLY
                # SUBTRACT ONE FROM QUANTITY
                condition = f'quantity = {quantity - 1}'
                where = f"Name = '{character_name}' AND weaponNameEN = '{weapon_name_en}'"
                Cn.update_function('inventory', condition, where)
        equip_item(character_name, lang)
    else:
        # IF THE PLAYER IS NOT EQUIPPING ANY WEAPONS, THEN EQUIP FROM INVENTORY
        if item_type == 1:
            condition = f"weapon_name = {weapon_name_en}, weapon_stat = {weapon_attribute_value}" \
                        f", weapon_type =  {weapon_attribute_type}"
        elif item_type == 2:
            condition = f"armor_name = {weapon_name_en}, armor_stat = {weapon_attribute_value}"
        where = f"Name = '{character_name}'"
        Cn.update_function('equiped', condition, where)
        where = f"name = '{character_name}' AND weaponNameEN = '{weapon_name_en}'"
        query_inventory = Cn.select_function('inventory', where)
        cod, name, slot_index, weapon_name_en, weapon_attribute_type, weapon_attribute_value, \
            weapon_name_pt_br, quantity, item_type = query_inventory[0]
        if quantity == 1:
            # IF THE WEAPON EQUIPED HAS ONLY ONE ON INVENTORY THEN DELETE AND
            # REORGANIZE THE SLOTINDEX
            where = f"name = '{character_name}' AND weaponNameEN = '{weapon_name_en}'"
            Cn.delete_function('inventory', where)
            where = f"name = '{character_name}'"
            query_inventory = Cn.select_function('inventory', where)
            for cod, name, slot_index, weapon_name_en, weapon_attribute_type, \
                weapon_attribute_value, weapon_name_pt_br, quantity, \
                    item_type in query_inventory:
                if slot_index == 0:
                    pass
                else:
                    # IF SLOTINDEX > 0 THEN PLAYER HAS MORE ITENS, SUBTRACT
                    # ONE FOR EACH SLOT INDEX
                    condition = f'SlotIndex = {slot_index - 1}'
                    where = f"Name = '{character_name}'"
                    Cn.update_function('inventory', condition, where)
                equip_item(character_name, lang)
        else:
            # PLAYER HAS MORE THEN ONE WEAPON, THEN ONLY NEED TO SUBTRACT ONE FROM QUANTITY
            condition = f'quantity = {quantity - 1}'
            where = f"Name = '{character_name}' AND weaponNameEN = '{weapon_name_en}'"
            Cn.update_function('equiped', condition, where)
        equip_item(character_name, lang)


def equip_item(character_name, lang):
    Dg.clear()
    sys.stdout.write('INVENTORY\n')
    close_inventory = 0
    where_character = f"name = '{character_name}'"
    try:
        query_inventory = Cn.select_function('inventory', where_character)
        for cod, name, slot_index, weapon_name_en, weapon_attribute_type, weapon_attribute_value, weapon_name_pt_br, \
                quantity, item_type in query_inventory:
            if lang == 0:
                string = ('SLOT:' + str(slot_index) + '   QUANTITY:' + str(quantity) + '   ' + str(
                    weapon_attribute_type)
                          + ':' + str(weapon_attribute_value) + '   NAME:' + str(weapon_name_en))
                sys.stdout.write(string + '\n')
            else:
                string = ('SLOT:' + str(slot_index) + '   QUANTITY:' + str(quantity) + '   ' + str(
                    weapon_attribute_type) + ':' +
                          str(weapon_attribute_value) + '   NAME:' + str(weapon_name_pt_br))
                sys.stdout.write(string + '\n')

        if len(query_inventory) == 1:
            exit_option = 1
        else:
            exit_option = len(query_inventory)
        sys.stdout.write(f'EXIT:{exit_option}' + '\n')
        sys.stdout.flush()
        while close_inventory < 1:
            option = input('Choose:')
            if int(option) == int(exit_option):
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
                        query_equip_itens(character_name, weapon_name, weapon_name_en, weapon_type, weapon_stat,
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
                                #IF THE ITEM QUANTITY IN INVENTORY IS ONE, NEED TO DELETE FROM INVENTORY AND
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
        close_inventory = 2
    except IndexError:
        # DONT HAVE ITENS IN INVENTORY TO LIST
        sys.stdout.write('Your Inventory is empty')
        sys.stdout.flush()


#print(equip_item('Egilhard', 1))
