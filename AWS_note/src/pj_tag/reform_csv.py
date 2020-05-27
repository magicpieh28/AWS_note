import csv
from pathlib import Path
from typing import List, Dict, OrderedDict, Tuple

from . import system_data_dir

raw_tag_csv = system_data_dir / 'editorial_part_tag_project.csv'


def arrange_tag_type(tag: str) -> str:
    return tag.replace('\n', ' ')


def standardize_empty_column(tag: str) -> str:
    return tag.replace('-', '')


def select_column(dict_row: OrderedDict) -> Tuple[List, List]:
    listed_dict_row = list(dict_row.items())
    return listed_dict_row[18], listed_dict_row[22:33]


def read_csv(raw_tag_csv: Path) -> Tuple[List, List]:
    with raw_tag_csv.open(mode='r') as tc:
        tc = csv.DictReader(tc, delimiter=',')
        for row in tc:
            yield select_column(row)


def build_news_tag(raw_tag_csv: Path, reformed_file_name: str) -> None:
    reformed_csv = system_data_dir / reformed_file_name
    header = ['news_id', 'tag_type', 'tag']

    with open(reformed_csv, mode='w', newline='') as rc:
        rc_dict_writer = csv.DictWriter(rc, fieldnames=header)
        rc_dict_writer.writeheader()

        for news_id, tags in read_csv(raw_tag_csv):
            for tag in tags:
                rc_dict_writer.writerow({
                    'news_id': news_id[1],
                    'tag_type': arrange_tag_type(tag[0]),
                    'tag': standardize_empty_column(tag[1])
                })


if __name__ == '__main__':
    # for news_id, tags in read_csv(raw_tag_csv):
    #     for tag in tags:
    #         print(news_id[1], rename_column(tag[0]), replace_empty_str(tag[1]))
    #     print('\n')

    build_news_tag(raw_tag_csv, 'refomed_tag_csv.csv')
