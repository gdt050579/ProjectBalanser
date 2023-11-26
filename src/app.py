
import pathlib
import argparse

from utils import logs


def get_arguments():
    parser = argparse.ArgumentParser(
        prog="Assigner",
        description="Assigning project to students by their preference on projects."
    )

    parser.add_argument("filepath", type=str, help="CSV File path of students preferences.")

    return parser.parse_args()


def main():
    logs.info("Started app")

    args = get_arguments()

    # Get students preferences file path
    students_preferences_file_path = pathlib.Path(args.filepath)

    logs.info(students_preferences_file_path)

    logs.info("Finished app")


if __name__ == "__main__":
    main()

