IMPORTANT!!! HOW TO RUN DATABASE ON YOUR MACHINE
1. Open XAMPP, then start the Apache and MySQL servers. 
2. Click the 'Admin' button in the MySQL row to bring up the PHPMyAdmin webpage.
3. Navigate to the 'User Accounts' tab, then click 'Add New User'.
4. Set the username to 'user' and the password to 'Password123$'. just copy/paste from here to prevent typos
5. Go down to 'Global Privileges' and check the 'Check All' box to give the account full admin perms.
6. Scroll down and hit 'Go' to create the account.
7. Go back to the main page, then to the 'Import' tab.
8. Hit 'Choose File', then navigate to the 'portalgame.sql' file in this PortalDatabase folder.
9. Scroll down and hit 'Import'.
10. Open command prompt as administrator, then run the commands 'pip install mysqlclient' and 'pip install mysql-connector'.
11. In VSCode, run 'LoginRegister.py'. If you see a list of a few registered users, everything was set up correctly.


----------------------------------------------
v   Database Structure   v
----------------------------------------------
PK = Primary Key
FK = Foreign Key

Table GameUser:
  int userID (PK)
  string username  <-- plaintext username
  string password  <-- hashed password

Table Level:
  int levelID (PK)
  string levelName
  int targetTime  <-- # of seconds to beat to recieve a star/medal

Table LevelTime: (Intersection table)
  int userID (FK PK)
  int levelID (FK PK)
  int completionTime  <-- # of seconds it took to beat the level

----------------------------------------------
v   Implementation Tips   v
----------------------------------------------
Users:
User data needs to be stored in the database, but passwords should not be exposed, because that is insecure. As a base level of security, the password should be hashed when the user creates their account. The username and hashed password is then stored in a new row of the GameUser table. When a user logs in, the input password should be hashed and compared against the hash stored in the database. If they match, the user logs in. If not, then they should be denied.

Levels:
There will need to be some correlation between how the levels are loaded in-game and how they are stored in the database. My suggestion is to store level data as text. Each level would be a .txt file with a grid of characters. Different characters represents a different object, such as an X for a non-portal-able tile, O for a portal-able tile, a space for an empty tile, etc. This would make creating, storing, and editing levels much easier than manually writing the position of every single tile in an array. Additionally, I could create a dev tool for us to view and design levels that would let you click to place tiles, and then export a file with the raw level data.

Updating Level Completion Times:
Both players need to have their completion times updated after they complete a level. 
First, check if there is an existing row in the LevelTime table for the current userID AND levelID. If there is, AND the new completion time is faster than the existing one, update that row with the new completionTime. If not, create a new row with the current userID, levelID, and completionTime.

