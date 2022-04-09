"""
Shiguys static site generator.

Svej Patel svejp@umich.edu
"""

from setuptools import setup

setup(
    name='shiguys_generator',
    version='0.1.0',
    packages=['shiguys_generator'],
    include_package_data=True,
    install_requires=[
        'bs4',
        'click',
        'html5validator',
        'jinja2',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'requests',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'shiguys_generator = shiguys_generator.__main__:main'
        ]
    },
)
