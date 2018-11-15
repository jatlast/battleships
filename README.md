# battleships

Battleships is the result of the following homework assignment.

Master's Degree: University of Michigan - Computer Science & Information Systems
Course: CSC 582 - Advanced Database Concepts

Assignment: Application Development Project: Due Nov 14, 11:59 pm
Choose a suitable language/technology/(ies) and implement connection to a database.
Once connected to the database, your code should do the following:
    (a)	Process (eg., display) multiple rows from a query result
    (b)	Have a multi-statement transaction, where all statements succeed and the transaction commits
    (c)	Have a multi-statement transaction, where the earlier statements succeed, and the later statement fails. In this case, the whole transaction must be rolled back.

## Preconceived Notions

1) All modern databases support Stored Procedures
2) All modern application development frameworks designed to work with databases support stored procedures.

## Chosen Technologies

Motivation: Become familiar with the following.
1) Developing on and for a Raspberry Pi B (or B+) using noting but Emacs
2) Creating an inexpensive but robust Web Server for the ARM architecture.
3) Developing with Python (3.6 or above - mostly due to "f-strings")
4) Any open source, Python Web framework (narrowed down to the following two)
    a) Flask (discarded after reading, "Pirates use Flask, the Navy uses Django")
    b) Django (used 2.1, but disappointed to discover its lacking stored procedure support)
5) Any open source database (ordered from least to most desirable)
    a) SQLite (settled for Sqlite3 because none of the three support stored procedures in any current version available for Raspberry Pi B boards and because I thought I would deploy on pythonanywhere.com with less installation difficulties)
    b) MySQL (aka, MariaDB)
    c) PostgreSQL
6) GitHub (a very powerful tool ignored for too long)
7) What has changed in Web development since my last efforts in 2009 (Back when the formula was C++ & Perl CGIs, MS-SQL DB, Flat HTML, a sprinkling of CSS, and a dash of JavaScript)?

## Getting Started

For old coders with a hint of Python experience - completely unfamiliar with today's Web Frameworks - having a go with Django Girl's Blog Tutorial is one of the many useful starting points (https://tutorial.djangogirls.org/en/).

### Prerequisites

- Raspberry Pi Model B (or B+) - Granted, this project should run on any OS since there is nothing specific to the ARM architecture within the code. 
- Python 3.6+
- Django 2.0+

### Installing

1) Install the "Battleships" project
2) Install the requirements (i.e., Django): $ pip3 install -r requirements.txt
3) activate virtual environment
    a) Linux: $ source myvenv/bin/activate
	b) Windows: $ myvenv\Scripts\activate
4) Create database superuser
    (myvenv) $ python manage.py createsuperuser
    a) if it works it means SQLite3 is already installed
    b) if it does not work it should install the SQLite3 DB
5) Initialize the database using the supplied initDB/initSQLite.sql file
    a) log into SQLite: $ sqlite3 db.sqlite3
    b) run the script: .read initDB/initSQLite.sql
6) Initialize the Django project for the freshly created SQLite DB
    a) $ python manage.py makemigrations
    b) $ python manage.py migrate
7) Start the Django Web server (substituting your local machine's IP): 
    (myvenv) $ python manage.py runserver 192.168.1.100:8000
8) Point a browser to your (hopefully) running Web instance of "Jason's Battleship"

It will not be accessable after this semester ends, however, anyone should be able to reach my currently running example: http://68.41.17.188:58201

## License

This project is not licensed but feel free to play with any part you so desire.

## Acknowledgments

* Django Girls
* Google's vast doorway into every tid-bit of documentation that is the Internet
* All those wonderfully generous documentation writers and question answerers
