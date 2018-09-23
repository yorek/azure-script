from setuptools import setup

setup(
    name='azsc',
    version='0.1',
    py_modules=['azsc'],
    install_requires=[
        'Click',
        'lark-parser==0.6.4'
    ],
    entry_points='''
        [console_scripts]
        azsc=azsc:cli
    ''',
)