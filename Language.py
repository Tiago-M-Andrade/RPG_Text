def login_language(lang):
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


def race_language(lang):
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


def location_system_language(lang, db_dialogues):
    # make a list with dialogues from database
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


def debuff_dictionary():
    debuff_text = {0: ['None', 'Nada'], 1: ['Decreased Movement Speed', 'Velocidade de Movimento Diminuída'],
                   2: ['Temporary Concussion', 'Concussão Temporaria'], 3: ['Poisoned', 'Envenenado']}
    return debuff_text


def test_skill_language(lang, character_class, skill_level, skill_name, skill_name_pt_br,
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


def calc_attack_language(lang):
    if lang == 0:
        crit_success_lang = 'Got critical success in the dices'
        crit_lang = 'Got Success in the dices'
        failure_lang = 'Got Failure in the dices'
        dead_text_lang = 'The enemy landed a blow on you and took {} damage, you died.'
        hit_text_lang = 'The enemy landed a blow on you and took {} damage, left {} life.'
        active_debuff = 'You have an active debuff, a d10 will be played and if the value is greater than 5 ' \
                        'you will hit the hit.'
        enemy_dead_lang = 'You hit the enemy and took {} damage, enemy defeated'
        enemy_hit_lang = 'You hit the enemy and took {} damage, left {} enemy life.'
        missed_hit_lang = 'You missed the attack.'
    else:
        crit_success_lang = 'Tirou sucesso critico nos dados'
        crit_lang = 'Tirou sucesso nos dados'
        failure_lang = 'Tirou falha nos dados'
        dead_text_lang = 'O inimigo acertou um golpe em você e tirou {} de dano, você morreu'
        hit_text_lang = 'O inimigo acertou um golpe em você e tirou {} de dano, restou {} de vida'
        active_debuff = 'Você tem um debuff ativo, será jogado um d10 e se o valor for maior que 5 você acertará o golpe'
        enemy_dead_lang = 'Você acertou o golpe no inimigo e tirou {} de dano, inimigo derrotado'
        enemy_hit_lang = 'Você acertou o golpe no inimigo e tirou {} de dano, restou {} de vida do inimigo'
        missed_hit_lang = 'Você errou o golpe'
    return crit_success_lang, crit_lang, failure_lang, dead_text_lang, hit_text_lang, active_debuff, enemy_dead_lang, enemy_hit_lang, missed_hit_lang


def attack_system_language(lang):
    if lang == 0:
        attack_text = 'You attacked {} [Space]'
        missed_attack = 'You missed the attack'
    else:
        attack_text = 'Você atacou {} [Espaço]'
        missed_attack = 'Você errou o golpe'
    return attack_text, missed_attack


def enemy_attack_language(lang):
    if lang == 0:
        attack_text = '{} attacked you\n'
        display_hit_calc = '{} hitted {} damage, you had {} defense, getting {}'
        enemy_missed_hit = '{} missed the hit.'
    else:
        attack_text = '{} atacou você\n'
        display_hit_calc = '{} tirou {} de dano, você tinha {} de defesa, ficando com {}'
        enemy_missed_hit = '{} errou o golpe.'
    return attack_text, display_hit_calc, enemy_missed_hit


def defense_system_language(lang):
    if lang == 0:
        try_defense_attack = 'You try to defend the attack from {} [Space]\n'
        crit_success_lang = 'You got a critical success on the dice and got {} of defense'
        crit_lang = 'You got a Success on the dice and got {} of defense'
        failure_lang = 'You got a failure on the dice and got the {} of defense'
        crit_failure_lang = "you couldn't defend yourself"
    else:
        try_defense_attack = 'Você tenta defender o ataque de {} [Espaço]\n'
        crit_success_lang = 'Tirou sucesso critico nos dados e ficou com {} de defesa'
        crit_lang = 'Tirou sucesso nos dados e ficou com {} de defesa'
        failure_lang = 'Tirou falha nos dados e ficou com {} de defesa'
        crit_failure_lang = 'Você não conseguiu se defender'
    return try_defense_attack, crit_success_lang, crit_lang, failure_lang, crit_failure_lang


def combat_language(lang):
    if lang == 0:
        start_text = 'What do you want to do? \n [0 - ATTACK]   [1 - DEFEND]  [2 - INVENTORY]'
        reaction_text = 'Enemy reacts to your attack and attacks back.'
        dead_text = 'You died.'
    else:
        start_text = 'O que deseja fazer? \n [0 - ATACAR]   [1 - DEFENDER]  [2 - INVENTÁRIO]'
        reaction_text = 'Inimigo reage ao seu ataque e ataca de volta.'
        dead_text = 'Você morreu.'
    return start_text, reaction_text, dead_text


def inventory_language(lang):
    if lang == 0:
        inventory_text = 'INVENTORY\n'
        slot_text = 'SLOT:'
        quantity_text = '   QUANTITY:'
        name_text = '   NAME:'
        exit_text = 'EXIT:{}\n'
        choose_text = 'Choose:'
        empty = 'Your Inventory is empty'
    else:
        inventory_text = 'INVENTÁRIO\n'
        slot_text = 'ESPAÇO:'
        quantity_text = '   QUANTIDADE:'
        name_text = '   NOME:'
        exit_text = 'SAIR:{}\n'
        choose_text = 'ESCOLHA:'
        empty = 'Seu inventário está vazio'
    return inventory_text, slot_text, quantity_text, name_text, exit_text, choose_text, empty
