import sqlite3

db = sqlite3.connect('database.db') # create/connect database
sql = db.cursor()

# Create table in database
sql.execute("""CREATE TABLE IF NOT EXISTS users ( 
    login TEXT,
    password TEXT,
    food BIGINT,
    clothes BIGINT,
    home BIGINT,
    entertainment BIGINT
)""")

db.commit() # save changes

def register_user():
    user_login = input("\n[*] Login >> ")
    user_password = input("[*] Password >> ")
    sql.execute("SELECT login FROM users WHERE login = ?", (user_login,)) # search login in table
    if sql.fetchone() is None:              # if there is no such a login - create new user
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (user_login, user_password, 0, 0, 0, 0))
        print("\n[#] Registration successful")
        db.commit()
        category(user_login, user_password) # go to the categories
    else:
        print("\n[!] Such a login already exists. Please try again later")
        main()                              # go to main menu

def login_user():
    user_login = input("\n[*] Login >> ")
    user_password = input("[*] Password >> ")
    sql.execute("SELECT * FROM users WHERE login = ? AND password = ?", (user_login, user_password,))
    
    if sql.fetchone():  # account verification
        print("\n[#] Login successful")
        category(user_login, user_password)
    else:
        print("\n[!] Wrong login or password. Please try again later")
        main()

def category(user_login, user_password):
    user_login = user_login
    user_password = user_password
    print("\n[#] Account: " + user_login)
    print("""
    Select category:
    1) Food
    2) Clothes
    3) Home
    4) Entertainment
    5) Statistics for all categories
    6) Statistics for one category
    7) Relogin
    8) Delete this user
    """)

    category_input = int(input("[*] >> ")) # select category

    if category_input == 5: 
        sql.execute("SELECT food, clothes, home, entertainment FROM users WHERE login = ?", (user_login,))
        costs = sql.fetchall()
        print("\n[#] Account: " + user_login)
        print("\n[#] All costs: " + str(sum(costs[0])))
        
        category(user_login, user_password)
    elif category_input == 6:
        print("\n[#] Account: " + user_login)
        print("\n[#] Costs by categories")

        sql.execute(f'SELECT food, clothes, home, entertainment FROM users WHERE login = "{user_login}"') 
        costs = sql.fetchall()

        for i in range(0, 4):
            print("[.] " + sql.description[i][0] + ": " + str(costs[0][i]))
        
        category(user_login, user_password)
    elif category_input == 7:
        login_user()

    elif category_input == 8: # deleting account
        db.execute(f'DELETE FROM users WHERE login = "{user_login}"')
        db.commit()
        print("[#] User \"" + user_login + "\" successfully deleted")
        main()

    elif category_input >= 1 and category_input <= 4:
        # select all costs for current user
        sql.execute(f'SELECT food, clothes, home, entertainment FROM users WHERE login = "{user_login}"')
        cost = sql.fetchall()
        print("[#] Enter cost:")
        cost_input = int(input("[*] >> "))
        if category_input == 1:
            sql.execute(f"UPDATE users SET food = {cost[0][category_input - 1] + cost_input} WHERE login = '{user_login}' ")
        elif category_input == 2:
            sql.execute(f"UPDATE users SET clothes = {cost[0][category_input - 1] + cost_input} WHERE login = '{user_login}' ")
        elif category_input == 3:
            sql.execute(f"UPDATE users SET home = {cost[0][category_input - 1] + cost_input} WHERE login = '{user_login}' ")
        elif category_input == 4:
            sql.execute(f"UPDATE users SET entertainment = {cost[0][category_input - 1] + cost_input} WHERE login = '{user_login}' ")
        
        db.commit()

        category(user_login, user_password)
    
    else: 
        print("[!] Error!")
        exit()

def main(): # the first function you see
    print("""
    [/] CTRL + C for exit

        Welcome to selfControl
        Select option:
        1) Registration
        2) Login""")
    user_input = int(input("[*] >> "))

    if user_input == 1:
        register_user()
    elif user_input == 2:
        login_user()
    else:
        print("[!] Error!")
        exit()

# this is to avoid showing input and interrupt errors  
try:
    main()
except KeyboardInterrupt:
    print("Exiting...")
except Exception:
    pass
