import environ
import gunicorn


env = environ.Env()
GUNICORN_SERVER_SOFTWARE = env("GUNICORN_SERVER_SOFTWARE")

gunicorn.SERVER_SOFTWARE = GUNICORN_SERVER_SOFTWARE
