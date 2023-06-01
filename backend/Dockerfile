# FROM alpine
FROM python:3.10
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3-opencv 




WORKDIR /app
ADD ./req.txt ./backend/req.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r backend/req.txt
ADD . ./backend


#COPY ../Detection Detection

#RUN pip install --no-cache-dir -r Detection/req_2.txt
# RUN --mount=type=cache,target=/root/.cache/pip 

EXPOSE 5000

CMD ["python3", "-m", "flask", "--app", "backend.main", "run", "--host=0.0.0.0"]