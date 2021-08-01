from setuptools import setup

setup(
    name='notify', 
    version='0.1.0-beta',
    py_modules=['notify'],
    install_requires=['click', 'toml'],
    entry_points='''
        [console_scripts]
        notify=notify:main
    '''
)
