from distutils.core import setup

setup(
    name="gdocker-ci",
    version="0.0.1",
    description="Cli prototype for continuous integration with the google cloud platform",
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

#gcloud compute --project "utopian-pen-801" instances create "docker-test-1" --zone "europe-west1-b" --machine-type "f1-micro" --network "default" --metadata "start-script=docker.sh" --image container-vm
