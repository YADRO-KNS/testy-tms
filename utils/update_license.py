# TestY TMS - Test Management System
# Copyright (C) 2022 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.

import argparse
import difflib
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')

__version__ = '0.1'

EXTENSIONS = ['py']

LICENSE_HEADER = """# TestY TMS - Test Management System
# Copyright (C) 2022 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.
"""


def check_ext(name: str):
    """
    Check the file extension and return True if the given file should have a license
    """
    parts = name.split('.')
    if parts[-1] in EXTENSIONS:
        return True
    return False


def main(cmd_args):
    found = []
    logging.info(f'Update License version {__version__}')
    logging.info(f'Process the extensions {",".join(EXTENSIONS)} in directory {cmd_args.directory}')
    # Get all files including nested directories
    for path, subdirs, files in os.walk(cmd_args.directory):
        for name in files:
            if check_ext(name):
                found.append(os.path.join(path, name))
    logging.info(f'Found {len(found)} files')
    lisense_lines = LICENSE_HEADER.split('\n')
    for file in found:
        license_required = False
        with open(file, 'r+') as w:
            content = w.read()
            lines = content.split('\n')
            if not lines:
                continue
            if lines[0].startswith('# Generated by Django'):
                continue
            if lines[0].startswith('#!'):
                continue
            if lines[0:len(lisense_lines)] != lisense_lines:
                diff = '\n'.join([line for line in difflib.unified_diff(lisense_lines, lines[0:len(lisense_lines)])])
                logging.exception(f'No correct license found for {file}:\n{diff}')
                license_required = True
            if cmd_args.update and license_required:
                logging.info(f'Adding the license header for {file}')
                content = LICENSE_HEADER + '\n' + content
                w.seek(0)
                w.write(content)
                logging.info(f'The license header added for {file}')


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--update',
        help='Update files without license',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--directory',
        help='Directory for looking files',
        type=str,
        default=False,
        required=True
    )
    main(parser.parse_args())
