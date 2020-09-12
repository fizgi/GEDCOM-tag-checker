""" A script to check the validity of a .ged file data.

    author: Fatih IZGI
    date: 09-Sep-2020
    python: v3.8.4
"""

from typing import List, Iterator

SUPPORTED_TAGS: List[str] = ['0 INDI', '1 NAME', '1 SEX', '1 BIRT', '1 DEAT', '1 FAMC',
                             '1 FAMS', '1 FAM', '1 MARR', '1 HUSB', '1 WIFE', '1 CHIL',
                             '1 DIV', '2 DATE', '0 HEAD', '0 TRLR', '0 NOTE']


def process_file(path: str) -> Iterator[str]:
    """ process data read from a .ged file """
    with (file := open(path, "r")):  # close file after opening
        for line in file:
            print('-->', line.rstrip("\n"))
            row_fields: List[str] = line.rstrip("\n").split(' ', 2)
            row_field_count: int = len(row_fields)

            level: str = row_fields[0]
            tag: str = row_fields[1]
            valid: str = 'Y' if f"{level} {tag}" in SUPPORTED_TAGS else 'N'  # verify LEVEL and TAG

            if row_field_count == 2:  # rows with only LEVEL and TAG (no arguments)
                yield f"<-- {'|'.join([level, tag, valid])}"
            elif row_fields[2] in ['INDI', 'FAM']:  # ID row, different format (overriding)
                _id: str = row_fields[1]
                tag: str = row_fields[2]
                valid: str = 'Y' if f"{level} {tag}" in SUPPORTED_TAGS else 'N'
                yield f"<-- {'|'.join([level, tag, valid, _id])}"
            else:  # rows with arguments
                args: str = row_fields[2]
                yield f"<-- {'|'.join([level, tag, valid, args])}"


def main():
    """ the main function to check the data """
    path: str = 'SSW555_GED_FatihIzgi.ged'  # path to .ged file

    for row in process_file(path):  # process the file
        print(row)


if __name__ == '__main__':
    main()
