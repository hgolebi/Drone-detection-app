from minio import Minio
from minio.error import S3Error
import tempfile
import os
import cv2
import numpy as np
import thumbnails

# minio_client = Minio(
#     'localhost:9000', access_key="tracking_system", secret_key="password", secure=False)


class MinioClient:
    def __init__(self, endpoint='localhost:9000', access_key="tracking_system", secret_key="password"):
        self._client = Minio(
            endpoint=endpoint, access_key=access_key, secret_key=secret_key, secure=False)
        self._bucket = None

    def set_client(self, user_id='01'):
        found = self._client.bucket_exists(f"user{user_id}")
        if not found:
            self._client.make_bucket(f"user{user_id}")
        self._bucket = f"user{user_id}"

    def put_thumbnail(self, videoname):
        if self._bucket is None:
            raise SyntaxError('User not select')

        thumbnails.generate_thumbnail(videoname)
        thumbname = thumbnails.thumbnail_name(videoname)

        self._client.fput_object(
            self._bucket, f"thumbnail/{thumbname}", f"./backend/tmp/{thumbname}")

        os.remove(f"./backend/tmp/{thumbname}")

    def get_thumbnail(self, videname):
        if self._bucket is None:
            raise SyntaxError('User not select')

        tmp = tempfile.NamedTemporaryFile()
        filename = thumbnails.thumbnail_name(videname)
        # self._client.get_object(
        #     self._bucket, filename, f"./backend/tmp/{filename}")
        try:
            response = self._client.get_object(
                self._bucket, f"thumbnail/{filename}")
            tmp.write(response.data)
        finally:
            response.close()
            response.release_conn()
        tmp.seek(0)
        return tmp

    def put_video(self, filename):
        if self._bucket is None:
            raise SyntaxError('User not select')

        # fp = tempfile.NamedTemporaryFile()
        # fp.write(data)
        # fp.seek(0)
        self.put_thumbnail(filename)

        self._client.fput_object(
            self._bucket, f"video/{filename}", f"./backend/tmp/{filename}")

        os.remove(f"./backend/tmp/{filename}")

    def _get_video(self, filename):
        if self._bucket is None:
            raise SyntaxError('User not select')
        tmp = tempfile.NamedTemporaryFile()
        # self._client.get_object(
        #     self._bucket, filename, f"./backend/tmp/{filename}")
        try:
            response = self._client.get_object(
                self._bucket, f"video/{filename}")
            tmp.write(response.data)

    # Read data from response.
        finally:
            response.close()
            response.release_conn()
        tmp.seek(0)
        return tmp

    def get_video(self, filename):
        return self._get_video(f"video/{filename}")

    def get_tracked(self, filename):
        return self._get_video(f"tracking/{filename}")
    #     if self._bucket is None:
    #         raise SyntaxError('User not select')
    #     tmp = tempfile.NamedTemporaryFile()
    #     # self._client.get_object(
    #     #     self._bucket, filename, f"./backend/tmp/{filename}")
    #     try:
    #         response = self._client.get_object(
    #             self._bucket, f"video/{filename}")
    #         tmp.write(response.data)

    # # Read data from response.
    #     finally:
    #         response.close()
    #         response.release_conn()
    #     tmp.seek(0)
    #     return tmp

    # def put_thumbnail(self, filename,  data):
    #     if self._bucket is None:
    #         raise SyntaxError('User not select')

    #     self._client.put_object(self._bucket, f"video/{filename}",
    #                             data=data, length=-1, part_size=10*1024*1024)

    def list_object(self):
        if self._bucket is None:
            raise SyntaxError('User not select')

        return self._client.list_objects(f"{self._bucket}", recursive=True, prefix='video/')

    def list_names(self):
        if self._bucket is None:
            raise SyntaxError('User not select')

        for o in self.list_object():
            yield o.object_name[6:]
        # next(objects)
        # yield


# found = minio_client.bucket_exists('dupa123')
# if not found:
#     minio_client.make_bucket('dupa123')
# else:
#     print('ddupa')

if __name__ == "__main__":
    client = MinioClient()

    client.set_client('03')
    print([i for i in client.list_names()])
    # tempdir=tempfile.TemporaryDirectory()
    a = client.get_video('Pensjonat_Bekas.mp4')
    print(a.name)
    image = thumbnails.generate_thumbnail(a)

    # print(image.shape)
    cv2.imwrite(
        f"./backend/tmp/{thumbnails.thumbnail_name('Pensjonat_Bekas.mp4')}", image)
    a.close()

    # client.put_object('film.mp4', './backend/uploads/GOPR5842_005.mp4')
    # client.get_object('Pensjonat_Bekas.mp4')
    # with client.get_object("film.mp4") as f:
    #     print(f.read())
    # c = client.list_names()
    # print([i for i in client.list_names()])
