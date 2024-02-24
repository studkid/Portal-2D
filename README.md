# Portal 2D &middot; Web III Project
> A two-player cooperative 2D puzzle game inspired by Portal.

Portal 2D is a game revolving around team-based puzzles in a side scrolling 2D environment with two players, 
while moving the players and items from one place to another in an innovative manner. 
Players can create portals to create a visual and physical connection between two different locations.
Players can either go or move items through the portals to solve puzzles.


## Developing

### Built With

Portal 2D will be developed using:

&middot; Python, Pygame - Creating game logic

&middot; Pygbag - Web integration for Pygame 

&middot; MySQL - Database for persistent data

### Prerequisites

Make sure that you have the latest version of Git, Python, Pygame, and Pygbag installed.

### Setting up Dev

Here's a brief intro about what a developer must do in order to start developing
the project:

Run this command to clone the repository to your machine.

```shell
git clone https://github.com/studkid/Portal-2D C:/Users/user/projectfolder
```

This will create a local copy of the repository's file structure to a location of your choice.

Open up Visual Studio Code, navigate to the newly cloned folder, and open it.

Click on the Source Control tab for GitHub-related features.

## Database

We will be using MySQL to store persistent data. The list of completed levels and the times of level completion for each player will 
be saved to the database. 

## Organization

&middot; **Use descriptive and consistent directory names** - The contents of a folder should be self-evident just from reading its name.

&middot; **Keep assest and code apart** - Game assets (e.g. music, artwork, or sound effects) should be kept into folders of their own, and should not be put into the same folder as code files.

&middot; **Split code into separate files** - Ideally, a single file should aim to do just one thing. If it's getting longer than a couple hundred lines, you should consider splitting it up for better readability and maintainability.

## Code Changes

Create a new branch for the task you're currently working on. 
When you get to the point that you're putting your task into the Review category, have someone review your code before merging it to the main branch. 
Leave comments on changes and what is and isn't working when pushing to your branch.
Don't push broken code to main. 

## Style Guide

Whenever possible, follow the Python code style - https://peps.python.org/pep-0008/

## External Reference

&middot; Python Documentation - https://docs.python.org/3/reference/index.html

&middot; Pygame Documentation - https://www.pygame.org/docs/ref/pygame.html

&middot; Pygbag Reference - https://pygame-web.github.io/

&middot; MySQL Documentation - https://dev.mysql.com/doc/refman/8.0/en/sql-statements.html
