from pathlib import Path

system_data_dir = Path.home() / 'data'
system_data_dir.mkdir(parents=True, exist_ok=True)
