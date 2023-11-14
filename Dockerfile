FROM python:3.10.10-slim

LABEL author='Oleh Borysevych'
LABEL email='borysevych.oleh87@gmail.com'

RUN apt-get update
RUN mkdir /app

COPY core streamlit_app.py requirements.txt /app/
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8080"]