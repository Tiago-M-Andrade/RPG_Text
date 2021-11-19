# LOGIN--------------------------------------------------------------------------
import time
from termcolor import colored


def login_text(lang):
    login = ''
    pass_w = ''
    logged = ''
    wrong_pass = ''
    success = ''
    create_account = ''
    if lang == 0:
        login = "Enter your character's name: "
        pass_w = 'Enter your password: '
        logged = 'Logged In'
        wrong_pass = 'Wrong Password'
        success = 'Your character {} was successfully created'
        create_account = '''Welcome {}, Would you like to create an account?\n [0 - YES]  [1 - NO]'''
    elif lang == 1:
        login = 'Digite o nome do seu personagem: '
        pass_w = 'Digite sua senha: '
        logged = 'Logado'
        wrong_pass = 'Senha Inválida'
        success = 'Seu personagem {} foi criado com sucesso'
        create_account = '''Bem-vindo {}, Gostaria de criar uma conta?\n [0 - SIM]  [1 - NÃO]'''
    return login, pass_w, logged, wrong_pass, success, create_account


def race_text(lang):
    races = []
    class_display = []
    choose = ''
    choose2 = ''
    success = ''
    if lang == 0:
        races = ['DWARF', 'ELF', 'GNOME', 'HALF-ELF', 'HALF-ORC', 'HALFLING', 'HUMAN']
        class_display = ['BARBARIAN', 'BARD', 'CLERIC', 'DRUID', 'FIGHTER', 'MONK', 'PALADIN', 'RANGER', 'ROGUE',
                         'WIZARD', 'MAGE']
        choose = 'Choose your race: '
        success = '{} chosen'
        choose2 = 'Choose your Class:'
    elif lang == 1:
        races = ['ANÃO', 'ELFO', 'GNOMO', 'MEIO-ELFO', 'MEIO-ORC', 'PEQUENINO', 'HUMANO']
        class_display = ['BARBARO', 'BARDO', 'CLÉRIGO', 'DRUIDA', 'LUTADOR', 'MONGE', 'PALADINO', 'GUARDA', 'LADINO',
                         'BRUXO', 'MAGO']
        choose = 'Escolha sua Raça: '
        success = '{} escolhido'
        choose2 = 'Escolha sua Classe:'
    return races, choose, success, class_display, choose2


def base_attributes_display(lang):
    strength = ''
    dexterity = ''
    constitution = ''
    intelligence = ''
    wisdom = ''
    charisma = ''
    message = ''
    if lang == 0:
        strength = 'STRENGTH'
        dexterity = 'DEXTERITY'
        constitution = 'CONSTITUTION'
        intelligence = 'INTELLIGENCE'
        wisdom = 'WISDOM'
        charisma = 'CHARISMA'
        message = 'Race {}, Base Attributes: STRENGTH {}, DEXTERITY {}, CONSTITUTION {}, INTELLIGENCE {}, WISDOM {}, ' \
                  'CHARISMA {} '
    elif lang == 1:
        strength = 'FORÇA'
        dexterity = 'AGILIDADE'
        constitution = 'CONSTITUIÇÃO'
        intelligence = 'INTELIGÊNCIA'
        wisdom = 'SABEDORIA'
        charisma = 'CARISMA'
        message = 'Raça {}, Atributos Base: FORÇA {}, AGILIDADE {}, CONSTITUIÇÃO {}, INTELIGÊNCIA {}, SABEDORIA {}, ' \
                  'CARISMA {} '
    return strength, dexterity, constitution, intelligence, wisdom, charisma, message


def location_system(lang, db_dialogues):
    dialogue_list = []
    for cod, location, text, language in db_dialogues:
        if language == lang:
            dialogue_list.append(text)
    return dialogue_list


def second_location_weapons():
    class_weapon = {'BARBARIAN': ['AXE', 'STR', 3, 'MACHADO'], 'BARD': ['SHORT SWORD', 'STR', 2, 'ESPADA CURTA'],
                    'CLERIC': ['ROUNDHEAD', 'STR', 3, 'MAÇA'], 'DRUID': ['DAGGER', 'DEX', 3, 'ADAGA'],
                    'FIGHTER': ['GAUNTLET', 'STR', 3, 'MANOPLA'], 'MONK': ['SHORT SWORD', 'STR', 2, 'ESPADA CURTA'],
                    'PALADIN': ['LONG SWORD', 'STR', 4, 'ESPADA LONGA'],
                    'RANGER': ['SHORT SWORD', 'STR', 2, 'ESPADA CURTA'], 'ROGUE': ['DAGGER', 'DEX', 3, 'ADAGA'],
                    'WIZARD': ['STAFF', 'INT', 3, 'CAJADO'], 'MAGE': ['WAND', 'INT', 4, 'VARINHA']}
    return class_weapon

def all_items():
    class_weapon = {'AXE': ['STR', 3, 'MACHADO'], 'SHORT_SWORD': ['STR', 2, 'ESPADA CURTA'],
                    'ROUNDHEAD': ['STR', 3, 'MAÇA'], 'DAGGER': ['DEX', 3, 'ADAGA'],
                    'GAUNTLET': ['STR', 3, 'MANOPLA'], 'LONG_SWORD': ['STR', 4, 'ESPADA LONGA'],
                    'STAFF': ['INT', 3, 'CAJADO'], 'WAND': ['INT', 4, 'VARINHA']}
    return class_weapon

def skills_dictionary():
    skills_text = {'ARCANE': ['ARCANE', 'ARCANISMO'], 'ACROBATIC': ['ACROBATIC', 'ACROBACIA'],
                   'ANIMAL HANDLING': ['ANIMAL HANDLING', 'ADESTRAR ANIMAIS'],
                   'ATHLETICS': ['ATHLETICS', 'ATLETISMO'], 'PERCEPTION': ['PERCEPTION', 'PERCEPÇÃO'],
                   'HISTORY': ['HISTORY', 'HISTÓRIA'], 'INSIGHT': ['INSIGHT', 'ENGANAÇÃO'],
                   'INTIMIDATION': ['INTIMIDATION', 'INTIMIDAÇÃO'],
                   'INVESTIGATION': ['INVESTIGATION', 'INVESTIGAÇÃO'], 'MEDICINE': ['MEDICINE', 'MEDICINA'],
                   'NATURE': ['NATURE', 'NATUREZA'],
                   'INTUITION': ['INTUITION', 'INTUIÇÃO'], 'PERSUASION': ['PERSUASION', 'PERSUASÃO'],
                   'PERFORMANCE': ['PERFORMANCE', 'ATUAÇÃO'],
                   'RELIGION': ['RELIGION', 'RELIGIÃO'], 'SLEIGHT OF HAND': ['SLEIGHT OF HAND', 'PRESTIDIGITAÇÃO'],
                   'STEALTH': ['STEALTH', 'FURTIVIDADE'], 'SURVIVAL': ['SURVIVAL', 'SOBREVIVÊNCIA']}
    return skills_text


def location_test_skill(lang, character_class, skill_level, skill_name, skill_name_pt_br,
                        character_base_attribute, db_dialogues):
    dialogue = db_dialogues[0][2]
    after_success = '\n' + db_dialogues[6][2]
    found = ''
    not_found = '\n' + db_dialogues[7][2]
    success_crit = ''
    success = db_dialogues[3][2] + f'[{skill_name}]'
    failure = db_dialogues[4][2]
    failure_crit = db_dialogues[5][2]
    result = ''
    luck_number = ''
    attribute = base_attributes_display(lang)
    base_attribute = attribute[character_base_attribute - 2]
    weapon_name_en, weapon_attr, weapon_attr_value, weapon_name_pt_br = second_location_weapons()[character_class]
    if lang == 0:
        success_crit = db_dialogues[1][2] + '\n' + db_dialogues[2][2] + f'[{skill_name}]'
        result = '\nThe result was D20 {} + D20 {} + ' + f'{base_attribute}' + ' {} = {} [Space]'
        if weapon_name_en == 'AXE':
            found = f'With your sharp eyesight you found an {weapon_name_en} [Space]'
        else:
            found = f'With your sharp eyesight you found a {weapon_name_en} [Space]'
        if skill_level + 0.5 >= 1:
            luck_number = f'\nYour skill in {skill_name} is level {skill_level + 0.5} so your lucky numbers are:' + '{}'
        else:
            luck_number = f'\nYour skill in {skill_name} is level {skill_level + 0.5} so your lucky number is:' + '{}'
    elif lang == 1:
        success_crit = db_dialogues[1][2] + '\n' + db_dialogues[2][2] + f'[{skill_name_pt_br}]'''
        result = '\nO resultado foi D20 {} + D20 {} + ' + f'{base_attribute}' + ' {} = {} [Espaço]'
        if weapon_name_pt_br == 'MACHADO':
            found = f'Com sua visão afiada vc encontrou um {weapon_name_pt_br} [Espaço]'
        else:
            found = f'Com sua visão afiada vc encontrou uma {weapon_name_pt_br} [Espaço]'
        if skill_level + 0.5 >= 1:
            luck_number = f'\nSua Pericia em {skill_name_pt_br} é nível {skill_level + 0.5} então seus números da sorte são:' + '{}'
        else:
            luck_number = f'\nSua Pericia em {skill_name_pt_br} é nível {skill_level + 0.5} então seu número da sorte é:' + '{}'
    return dialogue, success_crit, success, failure, failure_crit, result, after_success, found, not_found, luck_number
