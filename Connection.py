import keyboard as kb
import mysql.connector
import Dialogues as Dg
import Language as Lang


# Connection---------------------------------
def connection():
    """Make Connection to the game Database

              Return:\n
              the connection settings for Database
              """
    mysqldb = mysql.connector.connect(
        host="127.0.0.1",
        user="db_user",
        password="db_pass",
        port="3310",
        database="rpg"
    )
    return mysqldb


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
            Select: get the column name to query (Example: SlotIndex) \n
            How this look in function: SELECT MAX({Select}) AS maximum FROM {table} WHERE {where}  \n
            Example of result: SELECT MAX(SlotIndex) AS maximum FROM inventory WHERE Name = 'TEST'  \n
            Return:\n
            result the higher record from column selected
            """
    mysqldb = connection()
    dbcursor = mysqldb.cursor()

    dbcursor.execute(f"SELECT MAX({select}) AS maximum FROM {table} WHERE {where}")

    dbresult = dbcursor.fetchall()

    return dbresult


# Update------------------------------------

def update_function(table, condition, where):
    """Make Update in any table of the game Database

          Parameters:\n
          table: set the name of the table (Example: stats) \n
          condition: set the column names and values to update (Example: health_points = 120, attack = 60) \n
          where: set what records to update (Example: Name = 'TEST') \n
          How this look in function: UPDATE {table} SET {condition} WHERE {where} \n
          Example of result: UPDATE stats SET health_points = 120, attack = 60 WHERE Name = 'TEST' \n
          Return:\n
          result of the query if true then update was successful
          """
    mysqldb = connection()

    dbcursor = mysqldb.cursor()

    dbcursor.execute(f"UPDATE {table} SET {condition} WHERE {where}")

    mysqldb.commit()

    success = False
    if dbcursor.rowcount > 0:
        success = True
    return success


# Insert------------------------------------
def insert_function(table, *arg, **kwargs):
    """Make Insert in any table of the game Database

            Parameters:\n
            table: set the name of the table (Example: Race) \n
            *arg: set many fields you need to enter in Database (Example: 'Name', 'Race', 'Class') \n
            **kwargs: set many values you need to enter in Database, need to be the same quantity of *arg \n
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
              the character name, will be stored in a variable to be called in another's functions if needed
              """
    while status < 1:
        l, p, log, wrong, success, create_account = Lang.login_language(language)
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
    """Delete from in any table of the game Database

              Parameters:\n
              table: set the name of the table (Example: name) \n
              where: set what record want to delete (Example: Name = 'TEST') \n
              How this look in function: DELETE FROM {table} WHERE {where} \n
              Example of result: DELETE FROM name WHERE Name = 'TEST' \n
              Return:\n
              result of the query if true then delete was successful
              """
    mysqldb = connection()
    dbcursor = mysqldb.cursor()
    dbcursor.execute(f"DELETE FROM {table} WHERE {where}")
    mysqldb.commit()
    success = False
    if dbcursor.rowcount > 0:
        success = True
    return success
