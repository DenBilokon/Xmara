# Command_project_WEB_Django

![alt text](https://raw.githubusercontent.com/DenBilokon/Xmara/default/contacts_web_app/users/static/users/img/logo-no-background.png)

# "Personal Assistant" (Web application)
## Basic features of the web application:
- Save contacts with names, addresses, phone numbers, email and birthdays to the contact book, display a list of contacts whose birthday is a specified number of days from the current date;
- Save notes with text information, ssearch for notes, edit and delete notese, add "tags" to notes, keywords describing the topic and subject of the record, search and sort notes by keywords (tags).
- Upload user files to the cloud service and have access to them. Sort user files by categories (images, documents, videos, etc.) and display only the selected category (file filter by category).
- Provide a brief summary of news for the day (latest news, sport, war statistic, weather, currency).
## How to setup web app

- Clone the repository to your computer:

```sh
$ git clone https://github.com/DenBilokon/Xmara.git
$ cd contacts_web_app
```

- Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```
- Create your .env file using env.example.
- Install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```


Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd contacts_web_app
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

# Used technologies:
- Python 3.10
- Django 4.2.1
- BeautifulSoup 4
- Sphinx
- PostgreSQL 12.0
- OpenWeatherMap API
- OpenAI API
- Cloudinary
- Privatbank API
- Bootswatch
- HTML5
- CSS3
- Docker
- GitHub