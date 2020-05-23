from setuptools import setup

setup(
        name='pastemngr',
        description='A powerful pastebin manager for the command line.',
        version='1.0.0',
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


        packages=(
            'pastemngr',
            'pastemngr.api',
            'pastemngr.core',
            'pastemngr.db',
            'pastemngr.parser',
        ),

        requires='requests',
        python_requires='>=3.6',
)
