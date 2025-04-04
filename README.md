# dir-sync

Python script to sync directories one way to periodically.

## Features

- Syncs directories one way from source to replica
- Uses SHA-256 checksum to detect changes
- Keeps track of file hashes in a JSON file
- Logs all actions to a log file

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py <source_directory> <replica_directory> <interval>
```

Example:

```bash
python main.py test_source test_replica 60
```

## Testing

```bash
pytest tests/test_main.py
```

## Logging

Logs are saved to `sync.log`
