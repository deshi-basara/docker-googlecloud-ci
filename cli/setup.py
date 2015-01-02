from setuptools import setup

setup(
    name="gdocker-ci",
    version="0.0.1",
    description="Cli prototype for deploying with the google cloud platform and docker",
    author="Simon Schuster",
    author_email="simon.schuster@hs-furtwangen.de",
    url="https://github.com/deshi-basara/docker-googlecloud-ci",
    py_modules=["gdocker"],
    install_requires=[
        "Click",
    ],
    entry_points='''
        [console_scripts]
        gdocker=gdocker:cli
    '''
)