# Item Catalog Web Application
By Pathan Fayaz Ahammed Khan
This web application is a project for the Udacity Full Stack Nano Degree Program

## About
This project is mainly aimed to provide knowledge on the authorisation and authentication of a project.
It is a Web Application which provides a list of items within different categories as well as provide a user registration and authentication system. The Registered users will have the ability to post, modify, edit, and delete their own items.

## In This Project
This Project contains Data_Setup python file in which the database as well as the tables with columns are created.
The database_init python file is used to enter the data into the columns of the table in the database.
The main python file gives the internal configuration of the project such as adding, editing and deleting of categories as well as items in the categories.

## Skills and Tools Required
1. Python 2.7 or Python 3
2. HTML
3. CSS
4. OAuth
5. Flask Framework
6. DataBaseModels
This Project requires installation of tools like 
1. Vagrant
2. Virtual Box
Download these tools from the internet.

## Item Catalog Folder
This Folder Contains the following:
1. _pycache_
	1. Data_Setup.cpython-36
	2. Data_Setup.cpython-37
2. static
	1.styles.css
3. templates
	1. addMovie.html
	2. addMovieGenre.html
	3. admin_login.html
	4. admin_loginFail.html
	5. allmovies.html
	6. deleteMovie.html
	7. deleteMovieGenre.html
	8. editMovie.html
	9. editMovieGenre.html
	10. login.html
	11. mainpage.html
	12. movietitles.html
	13. myhome.html 
	14. nav.html
	15. sample.html
	16. showMovies.html
4. venv
	1. Include
	2. Lib
	3. Scripts
	4. tcl
5. client_secrets.json
6. Data_Setup.py
7. database_init.py
8. main.py
9. movies.db
10. README.md

## How to Run
1. First install Vagrant in your computer.
2. Now install Virtual Box.
3. Open command prompt in your Item Catalog folder.
3. Now first initialize the Vagrant using the command:
	$ vagrant 
4. Log into Vagrant VM (`vagrant ssh`)
5. Navigate to `cd /vagrant` as instructed in terminal
6. The app imports requests which is not on this vm. Run pip install requests
7. Setup application database `python /movie-zone/Data_Setup.py`
8. *Insert sample data `python /movie-zone/database_init.py`
9. Run application using `python /movie-zone/main.py`
10. Access the application locally using http://localhost:8000

*Optional step(s)

## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'Movie Zone'
7. Authorized JavaScript origins = 'http://localhost:8000'
8. Authorized redirect URIs = 'http://localhost:8000/login' && 'http://localhost:8000/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in movie-zone directory that you cloned from here
14. Run application using `python /movie_zone/main.py`

## JSON Endpoints
The following are open to the public:

Movie Catalog JSON: `/MovieZone/JSON`
    - Displays the whole movie genres catalog. Movie Genres and all movies.

Movie Categories JSON: `/movieZone/movieGenre/JSON`
    - Displays all Movie Genres
All Movie Items: `/movieZone/moviegenres/JSON`
	- Displays all Movie Items

Movie Genre JSON: `/MovieZone/<path:moviegenre>/moviegenres/JSON`
    - Displays Movies for a specific Movie Genre

Movie Genre Item JSON: `/MovieZone/<path:moviegenre>/<path:movieitem_name>/JSON`
    - Displays a specific Movie Details.