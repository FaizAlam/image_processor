web: gunicorn image_processor.wsgi --log-file -
worker: celery -A image_processor worker -l info
