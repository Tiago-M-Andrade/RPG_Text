import mysql.connector
import Language as Lang
import keyboard as kb
import Dialogues as Dg


# Connection---------------------------------
def connection():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="db_user",
        password="db_pass",
        port="3310",
        database="rpg"
    )
    return mydb


# Select------------------------------------
def select_function(table, where):
    """Make Select in any table of the game Database

          Parameters:\n
          table: get the name of the table (Example: name) \n
          where: get the condition to query (Example: Name = 'TEST') \n
          How this look in function: SELECT * FROM {table} WHERE {where} \n
          Example of result: SELECT * FROM name WHERE Name = 'TEST' \n
          Return:\n
          result of the query
          """
    mysqldb = connection()
    dbcursor = mysqldb.cursor()

    dbcursor.execute(f"SELECT * FROM {table} WHERE {where}")

    dbresult = dbcursor.fetchall()

    return dbresult


def select_index_inventory(table, where, select):
    """Make Select in any table of the game Database if you need the max value

            Parameters:\n
            table: get the name of the table (Example: name) \n
            where: get the condition to query (Example: Name = 'TEST') \n
            Select: get the type of select to query (Example: SELECT MAX(column_name) AS maximum) \n
            How this look in function: SELECT MAX({Select}) AS maximum FROM {table} WHERE {where}  \n
            Example of result: SELECT MAX(SlotIndex) AS maximum FROM inventory WHERE Name = 'TEST'  \n
            Return:\n
            result of the query
            """
    mysqldb = connection()
    dbcursor = mysqldb.cursor()

    dbcursor.execute(f"SELECT MAX({select}) AS maximum FROM {table} WHERE {where}")

    dbresult = dbcursor.fetchall()

    return dbresult


# Update------------------------------------

def update_function(table, condition, where):
    mysqldb = connection()

    dbcursor = mysqldb.cursor()

    dbcursor.execute(f"UPDATE {table} SET {condition} WHERE {where}")

    mysqldb.commit()

    success = False
    if dbcursor.rowcount > 0:
        success = True
    return success


def update_location(name, location):
    condition = f'Location = {location}'
    where = f"Name = '{name}'"
    update_function('name', condition, where)
    return True


# Insert------------------------------------
def insert_function(table, *arg, **kwargs):
    """Make Insert in any table of the game Database

            Parameters:\n
            table: get the name of the table (Example: Race) \n
            *arg: get many fields you need to enter in Database (Example: 'Name', 'Race', 'Class') \n
            **kwargs: get many values you need to enter in Database, need to be the same quantity of *arg \n
            (Example: name='Test', race='ELF', class='PALADIN')
            How this look in function: INSERT INTO {table} {final_arg} VALUES ({val}) \n
            Example of result: INSERT INTO Race (Name, Race, Class) VALUES ('Test', 'Elf', 'Paladin') \n
            Return:\n
            True if work's and False if have error in the arguments
            """
    mysqldb = connection()
    dbcursor = mysqldb.cursor()
    count_arg = len(arg)
    final_arg = ""
    if count_arg == 1:
        final_arg = str('(' + arg[0] + ')')
    else:
        for i in range(count_arg):
            if i == 0:
                final_arg = str('(' + arg[i] + ', ')
            elif i == count_arg - 1:
                final_arg += str(arg[i] + ')')
            else:
                final_arg += str(arg[i] + ',')
    kwarg_result = ''
    for args in kwargs.values():
        if kwarg_result == '':
            if args.isnumeric():
                kwarg_result = str("" + args + "")
            else:
                kwarg_result = str("'" + args + "'")
        else:
            if args.isnumeric():
                kwarg_result += str(", " + args + "")
            else:
                kwarg_result += str(", '" + args + "'")
    val = kwarg_result
    sql = f"INSERT INTO {table} {final_arg} VALUES ({val})"
    dbcursor.execute(sql)

    mysqldb.commit()
    success = False
    if dbcursor.rowcount > 0:
        success = True
    return success


# Login Character-------------------------------------------------
def login(status, language):
    """Make Login in the game

              Parameters:\n
              status: when open the game status is 0 when the function is called \n
              Language: get the language chosen by the player \n
              When the function is called, the player will need to input the character name and password \n
              the function will check if character exists and if the password is correct, if is then log in \n
              if not then character will be created \n
              Return:\n
              the character name, will be stored in a variable to be called in anothers functions if needed
              """
    while status < 1:
        l, p, log, wrong, success, create_account = Lang.login_text(language)
        name = input(str(l))
        pass_w = input(str(p))
        try:
            query = f"Name = '{name}' AND Pass = '{pass_w}'"
            result = select_function('name', query)
            cod, name_r, pass_wr, location = result[0]
            print(log)
            return name, location
        except IndexError:
            try:
                query = f"Name = '{name}'"
                result = select_function('name', query)
                cod, name_r, pass_wr, location = result[0]
                print(wrong)
                status = 0
            except IndexError:
                location = 0
                Dg.clear()
                print(create_account.format(name))
                while True:
                    if kb.is_pressed('0'):
                        insert_function('name', 'Name', 'Pass', 'location', name=f"{name}", passw=f"{pass_w}",
                                        Loc=f"{location}")
                        Dg.clear()
                        print(success.format(name))
                        return name, location
                    elif kb.is_pressed('1'):
                        exit()


def delete_function(table, where):
    mysqldb = connection()

    dbcursor = mysqldb.cursor()

    dbcursor.execute(f"DELETE FROM {table} WHERE {where}")

    mysqldb.commit()

    success = False
    if dbcursor.rowcount > 0:
        success = True
    return success
