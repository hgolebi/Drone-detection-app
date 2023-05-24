import os
import subprocess
# from MinioClient import MinioClient

absolute_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(absolute_path, './uploads')
THUMBNAIL_FOLDER = os.path.join(absolute_path, './thumbnails')


class Thumbnails:
    def __init__(self, minio_client) -> None:
        self.minio_client = minio_client

    def thumbnail_name(self, videoname: str):
        return "-".join(videoname.split('.'))+".png"

    def generate_thumbnail(self, videoname: str, n=100):
        thumb_name = self.thumbnail_name(videoname)
        cmd = ['ffmpeg', '-y', '-i', f'{UPLOAD_FOLDER}/{videoname}', '-vf', f'thumbnail=n={n}',
               '-frames:v', '1', f'{THUMBNAIL_FOLDER}/{thumb_name}', '-loglevel', 'quiet']
        subprocess.run(cmd, shell=False)

    def check_thumbnail(self, videname: str):
        thumb_name = self.thumbnail_name(videname)
        if not thumb_name in os.listdir(THUMBNAIL_FOLDER):
            self.generate_thumbnail(videname, 100)


# check_thumbnail("film.mp4")
