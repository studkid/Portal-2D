import mysql.connector #for database connection
import hashlib #for password encryption


try:
    #initialize the database
    mydb = mysql.connector.connect(
        host="localhost", # <---- can replace localhost with the ipv4 address of the machine hosting the server, but localhost works for testing
        user="root", # <---- username for the MySQL account. YOU MUST HAVE A PHPMYADMIN ACCOUNT WITH THIS USERNAME
        password="", # <---- password for the MySQL account.  YOU MUST HAVE A PHPMYADMIN ACCOUNT WITH THIS PASSWORD
        database="portalgame" # <---- password for the MySQL account.  YOU MUST HAVE THIS DATABASE IN PHPMYADMIN
    )
except:
    print("could not connect to the database. check if you have the xampp server running and the database imported")

def create_user(username, password):

    #hash the password
    password_bytes = str(password).encode("utf-8")
    hashed_password = hashlib.sha256(password_bytes).hexdigest() 

    #store the data as Tuples so they can be used in a query
    user_name = (username,)
    user_data = (username, hashed_password)      

    #create the queries with blank spaces for the data
    find_user = ("SELECT * FROM GameUser "
                "WHERE username = %s")
    add_user = ("INSERT INTO GameUser "
                "(username, password) "
                "VALUES (%s, %s)")
    
    #execute query and get the result
    cursor = mydb.cursor()
    cursor.execute(find_user, user_name)
    result = cursor.fetchall()

    #if the query comes back empty, the username is available and an account can be created
    if result == []:
        cursor = mydb.cursor()
        cursor.execute(add_user, user_data)
        mydb.commit()
        print("username available, creating account...")
        return True
    #if the query does NOT come back empty, there is already an account with that username
    else:
        print("there is already an account with that username")
        return False
    
def authenticate_user(username, password):

    #hash the password
    password_bytes = str(password).encode("utf-8")
    hashed_password = hashlib.sha256(password_bytes).hexdigest() 

    #store the data as a Tuples so it can be used in a query
    user_data = (username, hashed_password)      

    #create the query with blank spaces for the data
    find_user = ("SELECT * FROM GameUser "
                "WHERE username = %s AND password = %s")
    
    #execute query and get the result
    cursor = mydb.cursor()
    cursor.execute(find_user, user_data)
    result = cursor.fetchall()

    #if the query comes back empty, either the username or password is incorrect
    if result == []:
        print("incorrect username or password. login failed")
        return False
    #if the query does NOT come back empty, there is already an account with that username
    else:
        print("successfully authenticated. login complete")
        return True
    
def get_levels():
    #get an array of all levels
    get_levels = ("SELECT * FROM Level")
    
    #execute query and get the result
    cursor = mydb.cursor()
    cursor.execute(get_levels)
    result = cursor.fetchall()

    return result
    
def update_level_time(username, level_id, level_time):   

    user_id = -1

    #create the queries with blank spaces for the data
    get_user_id = ("SELECT * FROM GameUser "
                "WHERE username = %s")
    check_values = ("SELECT * FROM LevelTime "
                "WHERE userID = %s AND levelID = %s ")
    update_values = ("UPDATE LevelTime "
                "SET completionTime = %s "
                "WHERE userID = %s AND levelID = %s ")
    add_values = ("INSERT INTO LevelTime "
                "(userID, levelID, completionTime) "
                "VALUES (%s, %s, %s)")
    
    #execute first query and get the result
    cursor = mydb.cursor()
    get_user_id_data = (username,)
    cursor.execute(get_user_id, get_user_id_data)
    user_data = cursor.fetchall()

    #if the query comes back empty, the user is not logged in somehow (should be impossible)
    if user_data == []:
        print("ERROR: user not logged in, could not update level time.")
        return False
    #if the query does NOT come back empty, grab the userID
    else:
        user_id = user_data[0][0]

        #execute second query and get the result
        check_values_data = (user_id, level_id)
        cursor.execute(check_values, check_values_data)
        level_data = cursor.fetchall()

        #if the query comes back empty, the user has not completed the level before, so a new row must be made
        if level_data == []:
            add_values_data = (user_id, level_id, level_time)
            cursor.execute(add_values, add_values_data)
            mydb.commit()
            print("Level Complete! Adding new completion time to database...")
            return True
        #if the query does NOT come back empty, the user has completed the level before, so an existing row must be altered
        else:
            #if the new time is faster than the old time, update it in the database. otherwise, keep the old completion time
            if level_data[0][2] > level_time:
                update_values_data = (level_time, user_id, level_id)
                cursor.execute(update_values, update_values_data)
                mydb.commit()
                print("Level Complete! Updating completion time to your new best...") 
            else:
                print("Level Complete!") 
            return True

        

#get the users from the database
def list_users():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM GameUser")
    userlist = mycursor.fetchall()
    return userlist
