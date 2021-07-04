FROM python:3
ENV PYTHONUNBUFFERED=1
COPY ecommerce /app
WORKDIR /app
RUN pip install -r requirements.txt && \
    python manage.py makemigrations && \
    python manage.py migrate
EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
