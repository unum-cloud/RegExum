from typing import List, Optional, Dict, Generator, Set, Tuple, Sequence, Generator
import csv
from pathlib import Path
import sys
import os.path

from PyStorageHelpers.Edge import Edge
from PyStorageHelpers.Text import Text


def allow_big_csv_fields():
    """
        When dealing with big docs in ElasticSearch - 
        an error may occur when bulk-loading:
        >>> _csv.Error: field larger than field limit (131072)        
    """
    max_field_len = sys.maxsize
    while True:
        # decrease the max_field_len value by factor 10
        # as long as the OverflowError occurs.
        # https://stackoverflow.com/a/15063941/2766161
        try:
            csv.field_size_limit(max_field_len)
            break
        except OverflowError:
            max_field_len = int(max_field_len/10)

# region Texts


def yield_texts_from_csv(filepath: str, column: str = 'content', id_column: str = None) -> Generator[Text, None, None]:
    last_text = str()
    last_id = 0
    allow_big_csv_fields()

    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            new_id = str(row[id_column]) if id_column else (last_id + 1)
            new_text = str(row[column])

            if new_id != last_id:
                if len(last_text) > 0:
                    yield Text(last_id, last_text)
                last_id = new_id
                last_text = new_text
            else:
                last_text += new_text

        if len(last_text) > 0:
            yield Text(last_id, last_text)


def yield_texts_from_directory(directory: str) -> Generator[Text, None, None]:

    idx = 0
    for path in Path(directory).iterdir():
        yield Text.from_file(path=path, _id=idx)
        idx += 1


def import_texts(gdb, filepath: str, *args, **kwargs) -> int:

    if filepath.endswith('.csv'):
        if hasattr(gdb, 'add_from_csv'):
            return gdb.add_from_csv(filepath, *args, **kwargs)
        elif hasattr(gdb, 'add_stream'):
            return gdb.add_stream(yield_texts_from_csv(filepath, *args, **kwargs))

    elif os.path.isdir(filepath):
        if hasattr(gdb, 'add_from_directory'):
            return gdb.add_from_directory(filepath)
        elif hasattr(gdb, 'add_stream'):
            return gdb.add_stream(yield_texts_from_directory(filepath))

    return 0
