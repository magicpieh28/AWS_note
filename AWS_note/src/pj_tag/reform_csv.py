import csv
from pathlib import Path
from typing import List, Dict, OrderedDict, Tuple

from . import system_data_dir


def arrange_tag_type(tag: str) -> str:
    return tag.replace('\n', ' ')


def standardize_empty_column(tag: str) -> str:
    return tag.replace('-', '')


def arrange_split_point(listed_dict_tags: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    return [(tag_type, tag.replace(', ', ',')) for tag_type, tag in listed_dict_tags]


def select_column(dict_row: OrderedDict) -> Tuple[List, List]:
    listed_dict_row = list(dict_row.items())
    return listed_dict_row[18], arrange_split_point(listed_dict_row[22:33])


def read_csv(raw_tag_csv: Path) -> Tuple[List, List]:
    with raw_tag_csv.open(mode='r') as tc:
        tc = csv.DictReader(tc, delimiter=',')
        for row in tc:
            yield select_column(row)


def split_multi_tags(listed_dict_tags: List) -> List[Tuple[str, str]]:
    inserted_list_dict = {
        i: [(tag_type, split_tag) for split_tag in tag.split(',') if split_tag != '']
        for i, (tag_type, tag) in enumerate(listed_dict_tags) if len(tag.split(',')) > 1 for split_tag in tag.split(',')
    }
    print(inserted_list_dict)

    next_insert_start_point = 0
    if len(inserted_list_dict) > 0:
        for idx, (insert_start_idx, multi_tag_list) in enumerate(inserted_list_dict.items()):
            listed_dict_tags.pop(insert_start_idx + next_insert_start_point)

            for i in range(len(multi_tag_list)):
                insert_point = insert_start_idx + i
                if idx != 0:
                    insert_point = insert_start_idx + next_insert_start_point
                listed_dict_tags.insert(insert_point, multi_tag_list[i])

                if i != len(multi_tag_list) - 1:
                    next_insert_start_point += 1

    return listed_dict_tags


def build_news_tag(raw_tag_csv: Path, reformed_file_name: str) -> None:
    reformed_csv = system_data_dir / reformed_file_name
    header = ['news_id', 'tag_type', 'tag']

    with open(reformed_csv, mode='w', newline='') as rc:
        rc_dict_writer = csv.DictWriter(rc, fieldnames=header)
        rc_dict_writer.writeheader()

        for news_id, tags in read_csv(raw_tag_csv):
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

    # listed_dict_tags = [('5ジャンル', 'NewsPicks Business'), ('カテゴリ', 'ビジネス'), ('連載タイプ', '特集A'), ('記事タイプ', '記事'), ('地域', ''), ('tag1（業界）\n※SPEEDA参考', '総合商社'), ('tag2（企業名）', '‐'), ('tag2（特別単語）\n※カメリオの結果から特出すべき固有名詞', '総合商社,株式市場,合コン市場,投資,リターン'), ('tag3（登場人物）', ''), ('著者', ''), ('tag4\n※NPっぽいタグ', '')]
    # split_multi_tags(listed_dict_tags)

    build_news_tag(raw_tag_csv, 'refomed_tag_csv.csv')
