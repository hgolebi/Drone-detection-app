FROM python:3.10

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3-opencv

WORKDIR /app

COPY . ./Detection
RUN python3 -m pip install pip==21.1.1
RUN --mount=type=cache,target=/root/.cache \
    python3 -m pip install -r Detection/req-track.txt

EXPOSE 5000

CMD ["python3", "-m", "flask",  "--app", "Detection.server", "run", "--host=0.0.0.0"]