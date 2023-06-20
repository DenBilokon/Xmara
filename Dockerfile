FROM python:3.10-slim-buster

#ENV APP_HOME /app

#WORKDIR $APP_HOME
WORKDIR .

#COPY poetry.lock $APP_HOME/poetry.lock
#COPY pyproject.toml $APP_HOME/pyproject.toml

#COPY requirements.txt .

#COPY contacts_web_app .
COPY . .
#RUN pip install poetry
#RUN poetry config virtualenvs.create false && poetry install --only main

RUN pip install -r requirements.txt


EXPOSE 8000

CMD ["python", "contacts_web_app/manage.py", "runserver", "0.0.0.0:8000"]

