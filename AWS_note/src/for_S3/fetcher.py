import json
import boto3
from pathlib import Path
from typing import List, Optional, Tuple, Dict
import pandas as pd


class Fetcher:

    def __init__(self, bucket_name: str, obj_key: str):
        self.bucket_name = bucket_name
        self.obj_key = obj_key

        self.profile = 'development'

    def fetch_as_bytes(self) -> str:
        return boto3.Session(profile_name=self.profile).resource('s3').Object(
            self.bucket_name,
            self.obj_key
        ).get()['Body'].read()

    def fetch_as_df(
            self, dtype: Dict[int, str], compression: str = 'infer', header: Optional[str, bool, None] = None,
            names: Optional[Tuple, None] = None, parse_dates: Optional[List[int], None] = None
    ) -> pd.DataFrame:
        return pd.read_csv(
            f'S3://{self.bucket_name}/{self.obj_key}',
            dtype=dtype,
            compression=compression,
            header=header,
            names=names,
            parse_dates=parse_dates
        )

    def fetch_obj_list(self, profile_name: str):
        self.bucket = boto3.Session(profile_name=profile_name).resource('s3').Bucket(self.bucket_name)
        for summary in self.bucket.objects.filter(Prefix=self.obj_key):
            yield f"s3://{self.bucket_name}/{summary.key}"

    def get_dtype(self, dtype: List[str]):
        return {i: d for i, d in enumerate(dtype)}
