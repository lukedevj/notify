from setuptools import setup

setup(
    name='notify', version='0.1.0-beta',
    py_modules=['notify'],
    install_requires=[
        'click==8.0.1',
        'toml==0.10.2'
    ],
    entry_points='''
        [console_scripts]
        notify=notify:main
    '''
)