# FROM alpine
FROM python:3-alpine
RUN apk update
RUN apk upgrade
RUN apk add --no-cache ffmpeg




WORKDIR /app

COPY . ./backend
#COPY ../Detection Detection

#RUN pip install --no-cache-dir -r Detection/req_2.txt
# RUN --mount=type=cache,target=/root/.cache/pip 
RUN pip3 install --upgrade pip
RUN pip3 install flask flask_cors minio
EXPOSE 5000

CMD ["python3", "-m", "flask", "--app", "backend.main", "run", "--host=0.0.0.0"]