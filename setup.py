from setuptools import setup

setup(
    name='fedoraland',
    version='0.1.0',
    packages=['fedoraland'],
    entry_points={
        'console_scripts': [
            'fedoraland = fedoraland.__main__:main'
        ]
    })
