import mysql.connector

mydb = mysql.connector.connect(
  host="localhost", # <---- can replace localhost with the ipv4 address of the machine hosting the server, but localhost works for testing
  user="user", # <---- username for the MySQL account. YOU MUST HAVE A PHPMYADMIN ACCOUNT WITH THIS USERNAME
  password="Password123$", # <---- password for the MySQL account.  YOU MUST HAVE A PHPMYADMIN ACCOUNT WITH THIS PASSWORD
  database="portalgame" # <---- password for the MySQL account.  YOU MUST HAVE THIS DATABASE IN PHPMYADMIN
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM GameUser")

myresult = mycursor.fetchall()

# prints the user data to the console
for x in myresult:
  print(x)