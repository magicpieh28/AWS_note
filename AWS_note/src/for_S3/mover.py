import boto3

from AWS_note.src.for_S3.fetcher import Fetcher


class Mover:

    def __init__(self, profile_name):
        self.s3 = boto3.Session(profile_name=profile_name).resource('s3')

    def move(self, current_bucket: str, new_bucket: str, current_src_path: str, new_src_path: str) -> None:
        self._copy(current_bucket, new_bucket, current_src_path, new_src_path)
        self._delete(current_bucket, current_src_path)
        print(f'{current_bucket}/{current_src_path} moved to {new_bucket}/{new_src_path}.')

    def _copy(self, current_bucket, new_bucket, current_src_path, new_src_path):
        self.s3.Object(new_bucket, new_src_path).copy_from(current_bucket, current_src_path)

    def _delete(self, current_bucket, current_src_path):
        self.s3.Object(current_bucket, current_src_path).delete()
