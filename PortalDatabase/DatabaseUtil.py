import mysql.connector #for database connection
import hashlib #for password encryption


#initialize the database
mydb = mysql.connector.connect(
    host="localhost", # <---- can replace localhost with the ipv4 address of the machine hosting the server, but localhost works for testing
    user="user", # <---- username for the MySQL account. YOU MUST HAVE A PHPMYADMIN ACCOUNT WITH THIS USERNAME
    password="Password123$", # <---- password for the MySQL account.  YOU MUST HAVE A PHPMYADMIN ACCOUNT WITH THIS PASSWORD
    database="portalgame" # <---- password for the MySQL account.  YOU MUST HAVE THIS DATABASE IN PHPMYADMIN
)

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

#get the users from the database
def list_users():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM GameUser")
    userlist = mycursor.fetchall()
    return userlist