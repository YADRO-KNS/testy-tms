import json
from contextlib import contextmanager
from datetime import datetime
from typing import Any


def back_up(dict_to_backup, path, name):
    with open(f'{path}/{name}{datetime.now()}.json', 'w') as file:
        file.write(json.dumps(dict_to_backup, indent=2))


@contextmanager
def timer(function_name: str):
    start_time = datetime.now()
    yield
    print(f'{function_name} took: ', datetime.now() - start_time)


def split_list_by_chunks(src_list: list, chunk_size: int = 40):
    return [src_list[x:x + chunk_size] for x in range(0, len(src_list), chunk_size)]


def find_idx_by_key_value(key: str, value: Any, src_list: list):
    for idx, elem in enumerate(src_list):
        if elem[key] == value:
            return idx
