FROM python:3.12.1
ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=1
WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile
COPY . /app
EXPOSE 8080
WORKDIR /app/src
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8080"]

