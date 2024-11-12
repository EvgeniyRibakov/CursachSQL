import configparser
from typing import Dict


def config(filename: str = 'database.ini', section: str = 'postgressql') -> Dict[str, str]:
    parser = configparser.ConfigParser()

    with open(filename, 'r', encoding='utf-8') as file:
        parser.read_file(file)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db
