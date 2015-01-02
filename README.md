docker-googlecloud-ci
=====================

Basic Cli-prototype for using continuous integration with Docker and Google Compute Engine.


================
### Dependencies
The following dependencies are needed globally

* Python (2.7)
* Google Cloud SDK (~0.9.41)
* Docker (~1.0)

Dev dependencies
* Virtualenv (~1.11.6)


=========
### Setup

Create a new virtualenv with Python 2.7 and activate
```Shell
[cli]$  virtualenv -p /usr/bin/python2.7 venv
[cli]$  . venv/bin/activate
```

Install gdocker in your virtual environment
```Shell
(venv)[cli]$  python setup.py install

or (if you want to modify the code)

(venv)[cli]$  pip install --editable . 
```

Get your Google Cloud Platform SDK running and create a new project inside Google Developer Console
```Shell
# If you have more than one Python installation on your system &
# the default one is not 2.7
$ echo "export CLOUDSDK_PYTHON=/usr/bin/python2.7" >> ~/.bashrc && source ~/.bashrc

# Authenticate and generate your Google Cloud SSH keys
$ gcloud auth
$ gcloud compute config-ssh
```


============
### Workflow

Add your dependencies in your Dockerfile or copy them as files into the 'image/' folder
```Shell
# Example dependency
[image]$  echo "RUN     sudo apt-get install -y python" >> Dockerfile
```

Build your image and push it into your Docker Hub repo
```Shell
[image]$  sudo docker build -t <username>/gdocker-nodejs .
[image]$  sudo docker push <username>/gdocker-nodejs .
```

Initialise your gdocker-config inside your project folder
```Shell
# All values are optional and will be set with default values, except the last two arguments (repo-url, project-id)
[my-git-project]$   gdocker init --api_version "0.0.1" --start_scripts "start.sh" --gzone "europe-west1-b" \
		                --gmachine "f1-micro" --gimage "container-vm" -gport "1337" REPOSITORY_URL GOOGLE_PROJECT_ID
```

Create your start-script inside your repository and push it. (Your start-script will later be used to
start your application inside your docker-container).
```Shell
[my-git-project]$   echo "node app.js" >> start.sh
```

Deploy your project on the Google Compute Engine
```Shell
[my-git-project]$   gdocker deploy NEW_API_VERSION \
		                --commit "62b7281[...]edca1ba" # if you want to deploy a certain commit
```

If everything went right you should see
```Shell
[my-git-project]$   gdocker deploy 0.0.2

======================================================================
1/6 Deploying Container VM on Google Cloud Platform ...
======================================================================

[...]

======================================================================
2/6 Opening firewall ports on Container VM ...
======================================================================

[...]

======================================================================
3/6 Deploying Docker Image inside Container VM ...
======================================================================

[...]

======================================================================
4/6 Validating Input
======================================================================

[...]

======================================================================
5/6 Pulling Git-Rep
======================================================================

[...]

======================================================================
6/6 Upstarting the application
======================================================================

[...]

======================================================================
Success ... Application was deployed!
======================================================================

```


========
### Todo

* Stop a running instance and deploy on the same address