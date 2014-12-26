from ConfigParser import SafeConfigParser
from os import path
import sys
import subprocess
import click


class Config(object):
    """
    Global config object which holds all data from .docker.ini
    and manipulates it.
    """
    def __init__(self):
        # parse the config file
        self.config = SafeConfigParser()
        self.name = '.gdocker.ini'
        self.verbose = True
        self.deploy_cmd = []

    def create_config(self):
        # create a new '.gdocker.ini'
        with open(self.name, 'w') as file:
            # read the newly created file and write two sections into it
            self.config.read(self.name)
            self.config.add_section('repo')
            self.config.add_section('gcloud')
            self.config.write(file)
            if self.verbose:
                click.echo('Verbose: Initialising gdocker-config file inside current folder')

    def set_config(self, section, key, value):
        self.config.set(section, key, value)
        if self.verbose:
            click.echo('Verbose: Added to .gdocker.ini [%s=%s]' % (key, value))

    def write_config(self):
        with open(self.name, 'w') as config_file:
            self.config.write(config_file)
            if self.verbose:
                click.echo('Verbose: Config changes written to .gdocker.ini')

    def build_deploy_cmd(self):
        # read the config file
        self.config.read(self.name)
        # start command
        self.deploy_cmd.append("gcloud")
        self.deploy_cmd.append("compute")
        # append command options
        self.deploy_cmd.append("--project")
        self.deploy_cmd.append("" + self.config.get("gcloud", "project_id"))
        self.deploy_cmd.append("instances")
        self.deploy_cmd.append("create")
        self.deploy_cmd.append("docker-test-1")
        self.deploy_cmd.append("--zone")
        self.deploy_cmd.append("" + self.config.get("gcloud", "zone"))
        self.deploy_cmd.append("--machine-type")
        self.deploy_cmd.append("" + self.config.get("gcloud", "machine"))
        self.deploy_cmd.append("--network")
        self.deploy_cmd.append("default")
        self.deploy_cmd.append("--image")
        self.deploy_cmd.append("" + self.config.get("gcloud", "image"))
        # append meta data
        self.deploy_cmd.append("--metadata")
        self.deploy_cmd.append("url=" + self.config.get("repo", "url"))
        self.deploy_cmd.append("commit=")
        self.deploy_cmd.append("start=" + self.config.get("repo", "startup_script"))
        self.deploy_cmd.append("--metadata-from-file")
        self.deploy_cmd.append("google-container-manifest=container.yaml")
        return self.deploy_cmd

    def does_exist(self):
        return path.isfile(self.name)


# click decorator that passes the config-object to all functions with @pass_config.
pass_config = click.make_pass_decorator(Config)


@click.group()
@click.pass_context
def cli(ctx):
    """
    Cli prototype for using continuous integration with Docker and Google Container Engine.
    """
    # Create a config object and remember it as as the context object. From
    # this point onwards other commands can refer to it by using the
    # @pass_config decorator.
    ctx.obj = Config()


@cli.command()
@click.option('--api_version', default='0.0.1',
              help='Current version number of your git-project')
@click.option('--startup_script', default="start.sh",
              help='Script from you repository that will be executed after deployment')
@click.option('--gzone', default="europe-west1-b",
              help="Google cloud zone of your machine")
@click.option('--gmachine', default="f1-micro",
              help="Google cloud machine type")
@click.option('--gimage', default="container-vm",
              help="Google cloud image that will be used for deployment")
@click.argument('repository_url', required=True)
@click.argument('google_project_id', required=True)
@pass_config
def init(config, repository_url, google_project_id, api_version, startup_script,
         gzone, gmachine, gimage):
    """
    Initiates the .gdocker-config-file
    """
    # check if there is already a .docker.ini file
    if config.does_exist():
        # does exist, warn and exit
        click.echo("Error: There is already a .gdocker.ini existing, remove it before initialising")
        sys.exit()
    else:
        # no .docker.ini, create a new one
        config.create_config()

    # start parsing
    config.set_config("repo", "url", repository_url)
    config.set_config("repo", "api_version", api_version)
    config.set_config("repo", "startup_script", startup_script)
    config.set_config("gcloud", "project_id", google_project_id)
    config.set_config("gcloud", "zone", gzone)
    config.set_config("gcloud", "machine", gmachine)
    config.set_config("gcloud", "image", gimage)

    # write config
    config.write_config()


@cli.command()
@click.option('--commit', default="latest",
              help="Define a sha commit-string that will be deployed")
@click.argument("new_api_version", required=True)
@pass_config
def deploy(config, new_api_version, commit):
    """
    Deploys the latest build in your repository to the google cloud engine.
    If a commit was specified, the commit will be deployed.
    """
    # check if there is an existing .docker.ini file
    if not config.does_exist():
        # does not exist, warn and exit
        click.echo("Error: There is no .gdocker.ini existing, initialise it before deployment")
        sys.exit()

    # get all needed deployment values from the config
    deploy_cmd = config.build_deploy_cmd()
    click.echo(deploy_cmd)

    # start the vm
    deploy_process = subprocess.Popen(deploy_cmd, stdout=subprocess.PIPE)
    click.echo("======================================================================")
    click.echo("1/3 Deploying Container VM on Google Cloud Platform ...")
    click.echo("======================================================================")
    # block io until the vm is ready & print output
    while deploy_process.poll() is None:
        new_line = deploy_process.stdout.readline()
        print new_line

    # start our docker image on the vm
    click.echo("======================================================================")
    click.echo("2/3 Deploying Docker Image inside Container VM")
    click.echo("======================================================================")

    docker_cmd = ["gcloud", "compute", "ssh", "--zone", "europe-west1-b",
                  "docker-test-1", "--command", "'sudo docker run -d deshibasara/gdocker-nodejs sh /src/docker.sh'"]
    docker_process = subprocess.Popen(docker_cmd, stdout=subprocess.PIPE)
    # block io until the container is ready & print output
    while docker_process.poll() is None:
        new_line = docker_process.stdout.readline()
        print new_line

    click.echo("======================================================================")
    click.echo("Success ... Application was deployed!")
    click.echo("======================================================================")


