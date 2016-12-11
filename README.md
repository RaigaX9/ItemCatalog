# Item Catalog

## Introduction

This project is for the Full Stack Web Developer Nanodegree where I have to create an item
catalog website using Python Flask, SQLAlchemy, and Google
API for authentication. The type of item catalog I've
done for this is a Pokemon series location catalog.

## Technologies
- Python

- Flask

- SQLAlchemy

- Bootstrap

- Google API for Authentication

## Instructions
1. Install both Vagrant and VirtualBox 

2. Download/clone this repository.

3. Open the command prompt

4. Navigate to the the `vagrant` folder

5. Run `vagrant up` to start up vagrant

6. Run `vagrant ssh` to connect to vagrant

7. In vagrant, do `cd /vagrant` where all the main files are

8. Run `python databasesetup.py`

9. Run `python insertdata.py`

10. Run `python project.py`

11. Open the browser and go to `localhost:8080`

## JSON Endpoints
To access the JSON Endpoints, here are the following:

Categories JSON: `/category/<categoryID>/json`

Items JSON: `/category/<categoryID>/<itemID>/json`

Everything JSON: `/json`

## References

Udacity - Full Stack Foundation

Structure and format inspired by: [https://github.com/felipegalvao/item_catalog_udacity](https://github.com/felipegalvao/item_catalog_udacity)

[Flask main website and documentations](http://flask.pocoo.org/)

[Flask Tutorial](http://www.tutorialspoint.com/flask/)

[The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

[Using OAuth 2.0 for Web Server Applications](https://developers.google.com/api-client-library/python/auth/web-app)

[Python's SQLAlchemy and Object-Relational Mapping](http://pythoncentral.io/introductory-tutorial-python-sqlalchemy/)

[Flask SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)