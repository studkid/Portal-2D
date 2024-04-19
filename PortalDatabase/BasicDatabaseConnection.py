import mysql.connector
import DatabaseUtil

mydb = mysql.connector.connect(
  host="localhost", # <---- can replace localhost with the ipv4 address of the machine hosting the server, but localhost works for testing
  user="root", # <---- username for the MySQL account. YOU MUST HAVE A PHPMYADMIN ACCOUNT WITH THIS USERNAME
  password="", # <---- password for the MySQL account.  YOU MUST HAVE A PHPMYADMIN ACCOUNT WITH THIS PASSWORD
  database="portalgame" # <---- password for the MySQL account.  YOU MUST HAVE THIS DATABASE IN PHPMYADMIN
)

#mycursor = mydb.cursor()

#mycursor.execute("SELECT * FROM GameUser")
#myresult = mycursor.fetchall()

# prints the user data to the console
#for x in myresult:
#  print(x)

#if a user has no saved completion time for a level ID, it will make a new row in the database. 
#if a user does have a saved completion time for that level, then it will only be updated if the new time is faster than the existing one
#DatabaseUtil.update_level_time("Admin", 1, 9)
#DatabaseUtil.update_level_time("Joe", 1, 42)

#returns an array of levels with the ID, levelname, and target time
levels = DatabaseUtil.get_levels()
for level in levels:
  print(level)