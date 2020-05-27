import pandas as pd
import pyarrow as pa
from pathlib import Path
import pyarrow.parquet as pq

from . import system_data_dir


def csv2parquet(reformed_csv: Path, parquet_file: Path) -> None :
    dataframe = pd.read_csv(reformed_csv)
    table = pa.Table.from_pandas(df=dataframe)
    pq.write_table(table, parquet_file)


def read_parquet(parquet_file: Path) -> None:
    table = pq.read_table(parquet_file)
    dataframe = table.to_pandas()
    print(dataframe)


if __name__ == '__main__':
    reformed_csv = system_data_dir / 'refomed_tag_csv.csv'
    parquet_file = system_data_dir / 'editorial_part_tags.pq'
    # csv2parquet(reformed_csv, parquet_file)
    read_parquet(parquet_file)
