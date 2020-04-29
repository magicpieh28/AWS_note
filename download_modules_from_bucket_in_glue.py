import os
from typing import Dict, List, Tuple


class InstallModules:
    def __init__(self, bucket, *src_paths: str):
        self.src_paths = [path for path in src_paths]
        self.module_names = [path.split('/')[-1] for path in src_paths]
        self.module_types = [path.split('.')[-1] for path in src_paths]

        self.non_zip_modules, self.zip_modules = self.classify_modules_by_type()

        self.bucket = bucket

    def classify_modules_by_type(self) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        non_zip_modules = []
        zip_modules = []

        for i, module_type in enumerate(self.module_types):
            if module_type == 'py' or module_type == 'sql':
                non_zip_modules.append((self.src_paths[i], self.module_names[i]))
            else:
                zip_modules.append((self.src_paths[i], self.module_names[i]))

        return non_zip_modules, zip_modules

    def download_file(self, module_info: Tuple[str, str]):
        self.bucket.download_file(module_info[0], module_info[1])

    def download_py_module(self, module_info: Tuple[str, str]):
        self.download_file(module_info)
        print('{0} is installed'.format(module_info[1]))

    def download_zip_module(self, module_info: Tuple[str, str]):
        self.download_file(module_info)
        os.system('unzip {0}'.format(module_info[1]))
        print('{0} is installed'.format(module_info[1]))

    def download_modules(self):
        if len(self.non_zip_modules) != 0:
            for python_module in self.non_zip_modules:
                self.download_py_module(python_module)

        if len(self.zip_modules) != 0:
            for zip_module in self.zip_modules:
                self.download_zip_module(zip_module)

    # TODO uploadのためのメソッド作らねば


if __name__ == '__main__':
    psycopg2 = 'codes/psycopg2.zip'
    auth = 'codes/src/authentication.py'
    pymysql = 'codes/pymysql.zip'
    python2 = 'codes/src/lib/python2.py'

    installer = InstallModules(psycopg2, auth, pymysql, python2)
    installer.download_modules()
    print(f'installer.src_pathes => {installer.src_paths}')
    print(f'installer.module_names => {installer.module_names}')
    print(f'installer.module_types => {installer.module_types}')
    print(f'installer.python_modules => {installer.python_modules}')
    print(f'installer.zip_modules => {installer.zip_modules}')
