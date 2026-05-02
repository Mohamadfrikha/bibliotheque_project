FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV SECRET_KEY="build-time-dummy-key" \
    POSTGRES_DB="postgres" \
    POSTGRES_USER="postgres" \
    POSTGRES_PASSWORD="postgres" \
    POSTGRES_HOST="postgres-service" \
    STRIPE_SECRET_KEY="dummy" \
    STRIPE_PUBLISHABLE_KEY="dummy"
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bibliotheque_project.wsgi:application"]