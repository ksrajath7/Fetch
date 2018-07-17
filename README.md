# Fetch
#### Data fetching utility for crawling online travel websites.
Fetch is a web application made using Flask. It helps you access flight information like price, duration and date. 
It also lets you export the data in csv, xlsx or txt formats.

##### Built With
* Flask
* jQuery
* SQLAlchemy
* Bootstrap


##### Prerequisites
* Python 3.6
* pip

##### Setting up environment
```
git clone git@github.com:naveencode/Fetch.git
pip install pipenv
cd Fetch
pipenv install --python 3.6
pipenv shell
flask run
```

##### Configuration
* DATABASE_URL = *Your database URI*
* API_KEY = *Amadeus API key*
* FLASK_APP=app

##### Api Reference
https://developers.amadeus.com/self-service/category/203/api-doc/4/api-docs-and-example/10002

##### Database
* Postgresql (9.5)
https://www.postgresql.org/docs/9.5/static/release-9-5.html

##### Models
* Journey
* Itinerary
* Flight




