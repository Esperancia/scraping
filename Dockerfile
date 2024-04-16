FROM python:3.10
COPY . .
WORKDIR .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#RUN python3 -m venv .venv
ENTRYPOINT python3 main.py
EXPOSE 5000
