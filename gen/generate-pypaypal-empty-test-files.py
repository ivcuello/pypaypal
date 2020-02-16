import os

template = r"""
'''test module for pypaypal.entities.{archive_name}
'''

import unittest

# TODO: Write tests here

if __name__ == '__main__':
    unittest.main()
""".replace('\'\'\'', '"""')

def create_template(directory: str):
    for archive in os.listdir(directory):
        path = directory+ '\\' + archive
        if os.path.isfile(path):
            with open(path, 'w') as of:
                of.writelines(template.replace('{archive_name}', archive.replace('.py','')))

def create_template_file(path: str, file_name: str):
    path = path + '\\' + file_name
    if os.path.isfile(path):
        with open(path, 'w') as of:
            of.writelines(template.replace('{archive_name}', file_name.replace('.py','')))