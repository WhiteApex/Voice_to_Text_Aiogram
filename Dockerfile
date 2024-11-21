FROM python:3.12

ENV TOKEN=YOUR_TG_TOKEN

RUN apt-get update && apt-get install -y --fix-missing ffmpeg

COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r req.txt

COPY . /usr/src/app

CMD ["python", "main.py"]