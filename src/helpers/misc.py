import os
from datetime import datetime, timezone


def ensure_env_var(name: str) -> str:
    value = os.getenv(name)

    if (not value == None) and (len(value) == 0):
        raise ValueError(f"{name} is missing in .env file")

    return value


def convert_to_timestamp(date_string):
    # Parse the input date string into a datetime object and set the timezone to UTC
    return int(
        datetime.strptime(date_string, "%Y/%m/%d %H:%M:%S")
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )


def count_file_operations(files):
    operations = {"add": 0, "edit": 0, "delete": 0}

    for file, revision_number, operation in files:
        # Ensure the operation is valid (add, edit, or delete)
        # there seem to be more like (move/add, move/delete) which we are not tracking
        if operation in operations:
            operations[operation] += 1

    return operations
