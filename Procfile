web: gunicorn movie_recommendation.wsgi:application --log-file - --log-level info
release: python manage.py migrate --noinput

