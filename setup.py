import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as rd:
    long_description = rd.read()

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as r:
    install_requires = r.read().splitlines()

setup(
        name='pastemngr',
        description='A powerful pastebin manager for the command line.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        version='1.0.5',
        author='pvpscript',
        url='https://github.com/pvpscript/pastemngr',
        keywords='pastebin manager console',

        classifiers=[
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: Unix',
            'Programming Language :: Python :: 3',
            'Topic :: Utilities',
        ],

        scripts=['scripts/pastemngr'],

        data_files=[
            ('share/man/man1', [
                'doc/pastemngr.1',
            ]),
            ('share/doc/pastemngr', [
                'README.md',
            ]),
        ],

        package_data = {
            'pastemngr': [
                'db/model.sql',
            ],
        },

        packages=(
            'pastemngr',
            'pastemngr.api',
            'pastemngr.core',
            'pastemngr.db',
            'pastemngr.parser',
        ),

        requires=install_requires,
        python_requires='>=3.6',
)
