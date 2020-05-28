import csv
from pathlib import Path
from typing import List, Dict, OrderedDict, Tuple

from . import system_data_dir


def arrange_tag_type(tag: str) -> str:
    return tag.replace('\n', ' ')


def standardize_empty_column(tag: str) -> str:
    return tag.replace('‐', '').replace('-', '')


def arrange_split_point(listed_tag_attr_pair: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    return [(tag_type, tag.replace(', ', ',')) for tag_type, tag in listed_tag_attr_pair]


def select_column(record: OrderedDict, id_idx: int, tags_range: Tuple[int, int])\
        -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:

    listed_tag_attr_pair = list(record.items())
    return listed_tag_attr_pair[id_idx], arrange_split_point(listed_tag_attr_pair[tags_range[0]:tags_range[1]+1])


def read_csv(raw_news_tag_csv: Path, id_idx: int, tags_range: Tuple[int, int]) \
        -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:

    with raw_news_tag_csv.open(mode='r') as tc:
        tc = csv.DictReader(tc, delimiter=',')
        for row in tc:
            yield select_column(row, id_idx, tags_range)


def split_multi_tags(listed_tag_attr_pair: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    divided_multi_tags_dict = {
        i: [(tag_type, split_tag) for split_tag in tag.split(',') if split_tag != '']
        for i, (tag_type, tag) in enumerate(listed_tag_attr_pair) if len(tag.split(',')) > 1
        for split_tag in tag.split(',')
    }

    pushed_idx_by_insert = 0
    if len(divided_multi_tags_dict) > 0:
        for idx, (insert_start_idx, multi_tag_list) in enumerate(divided_multi_tags_dict.items()):
            listed_tag_attr_pair.pop(insert_start_idx + pushed_idx_by_insert)

            for i in range(len(multi_tag_list)):

                insert_point = insert_start_idx + i
                if idx != 0:
                    insert_point = insert_start_idx + pushed_idx_by_insert

                listed_tag_attr_pair.insert(insert_point, multi_tag_list[i])

                if i != len(multi_tag_list) - 1:
                    pushed_idx_by_insert += 1

    return listed_tag_attr_pair


def build_news_tag(raw_news_tag_csv: Path, reformed_csv_name: str, id_idx: int, tags_range: Tuple[int, int]) -> None:
    reformed_csv = system_data_dir / reformed_csv_name
    header = ['news_id', 'tag_type', 'tag']

    with open(reformed_csv, mode='w', newline='') as rc:
        rc_dict_writer = csv.DictWriter(rc, fieldnames=header)
        rc_dict_writer.writeheader()

        for news_id, tags in read_csv(raw_news_tag_csv, id_idx, tags_range):
            tags = split_multi_tags(tags)
            for tag in tags:
                rc_dict_writer.writerow({
                    'news_id': news_id[1],
                    'tag_type': arrange_tag_type(tag[0]),
                    'tag': standardize_empty_column(tag[1])
                })


if __name__ == '__main__':
    raw_tag_csv = system_data_dir / 'editorial_part_tag_project.csv'

    # for news_id, tags in read_csv(raw_tag_csv):
    #     print(tags)
    #     for tag in tags:
    #         print(standardize_empty_column(tag[1]))
    #     print('\n')

    # split_multi_tags(listed_dict_tags)

    build_news_tag(raw_tag_csv, 'reformed_tag_csv.csv', 18, (22, 32))
