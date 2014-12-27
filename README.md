docker-googlecloud-ci
=====================

Cli prototype for using continuous integration with Docker and Google Container Engine


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
```

Get your Google Cloud Platform SDK running and create a new project inside Google Developer Console
```Shell
# If you have more than one Python installation on your system & the default one is not 2.7
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
[image]$  sudo docker build <username>/gdocker-nodejs .
[image]$  sudo docker push <username>/gdocker-nodejs .
```

Initialise your gdocker-config inside your project folder
```Shell
# All values are optional and will be set with default values, except the last two arguments (repo-url, project-id)
[my-git-project]$   gdocker init --api_version "0.0.1" --start_scripts "start.sh" --gzone "europe-west1-b" \
		                --gmachine "f1-micro" --gimage "container-vm" REPOSITORY_URL GOOGLE_PROJECT_ID
```

Create your start-script inside your repository and push it. (Your start-script will later be used to
start your application inside your docker-container).
```Shell
#
[my-git-project]$   echo "node app.js" >> start.sh
```

Deploy your project on the Google Compute Engine
```Shell
#
[my-git-project]$   gdocker deploy NEW_API_VERSION \
		                --commit "62b7281[...]edca1ba" # if you want to deploy a certain commit
```

If everything went right you should see
```Shell
#
[my-git-project]$   gdocker deploy 0.0.2

======================================================================
1/5 Deploying Container VM on Google Cloud Platform ...
======================================================================

[...]

======================================================================
2/5 Deploying Docker Image inside Container VM ...
======================================================================

[...]

======================================================================
3/5 Validating Input
======================================================================

[...]

======================================================================
4/5 Pulling Git-Rep
======================================================================

[...]

======================================================================
5/5 Upstarting the application
======================================================================

[...]

======================================================================
Success ... Application was deployed!
======================================================================

```


========
### Todo

* Project Version incrementation
* Stop a running instance and deploy on the same address