from sys import argv

from src.DoremiSubscription import DoremiSubscription
from src.helpers import read_file


def main(filepath: str):
    file_contents = read_file(filepath)

    _obj = DoremiSubscription()
    for row in file_contents:
        # remove new line characters
        row = row.replace("\n", "")
        # split the row into command and arguments
        row = row.split(" ")
        # get the command and arguments from the row
        command, args = row[0], row[1:]
        command_result = _obj.run_command(command, *args)
        # print command_result only if not none
        if command_result:
            is_list = isinstance(command_result, list)
            is_bool = isinstance(command_result, bool)
            # print(command_result, is_list, is_bool)

            # returning boolean to indicate that the command execution succeeded
            # printing only non boolean values
            if not is_bool:
                print(*command_result if is_list else command_result, sep="\n" if is_list else "")


if __name__ == '__main__':
    # Add file path here to execute the tests
    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    main(file_path)
