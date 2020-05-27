import re

from boto3.session import Session


class ParameterFetcher:
    def __init__(self, profile_name: str = 'default'):
        session = Session(profile_name=profile_name)
        self.ssm = session.client(service_name='ssm')

    def fetch_parameters(self, hierarchy_path: str) -> str:
        return self.ssm.get_parameter(
            Name=hierarchy_path,
            WithDecryption=True
        )['Parameters']['Value']
