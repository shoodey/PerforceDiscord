# Fetches the revision description from the perforce server for the given revision number
import re
import subprocess

from helpers.misc import convert_to_timestamp


def describe_revision(revision: int) -> str:
    description = subprocess.Popen(
        "p4 describe -s " + str(revision),
        shell=True,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    ).communicate()[0]

    return description


def parse_description(revision_description: str) -> str:
    # Split the description into lines and remove empty lines
    parsed_description = [
        line.strip() for line in revision_description.split("\n") if line.strip()
    ]

    if not len(parsed_description) > 0 and not parsed_description[0].startswith(
        "Change "
    ):
        raise ValueError("Invalid revision description")

    # Remove the "#changelist validated" line if it exists
    if "#changelist validated" in parsed_description:
        parsed_description.remove("#changelist validated")

    # Find the index of the line that starts the list of affected files
    # It delimits the end of the message and the start of the files list
    files_list_start = parsed_description.index("Affected files ...") + 1

    # Get datetime and convert it to timestamp
    datetime_str = (
        parsed_description[0].split()[5] + " " + parsed_description[0].split()[6]
    )
    timestamp = convert_to_timestamp(datetime_str)

    return {
        "revision_number": int(parsed_description[0].split()[1]),
        "author": parsed_description[0].split()[3].split("@")[0],
        "workspace": parsed_description[0].split()[3].split("@")[1],
        "timestamp": timestamp,
        "message": parsed_description[1 : files_list_start - 1],
        "files": parse_files_list(parsed_description[files_list_start:]),
    }


def parse_file_info(file_info):
    # Remove the ellipsis at the beginning of the line
    file_info = file_info[4:]

    # Define a regular expression pattern to match the desired parts
    pattern = r"#(\d+)\s+(\w+)"

    # Use re.search() to find the pattern in the string
    match = re.search(pattern, file_info)

    # If match is found, extract the operation and the number
    if match:
        operation = match.group(2)
        revision_number = match.group(1)

        # Remove the matched substring from the original string
        file_path = re.sub(pattern, "", file_info)

        return file_path.strip(), revision_number, operation
    else:
        return file_info.strip(), None, None


def parse_files_list(lines):
    parsed_lines = []
    for line in lines:
        parsed_lines.append(parse_file_info(line))
    return parsed_lines
