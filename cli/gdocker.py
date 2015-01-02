from ConfigParser import SafeConfigParser
from os import path
import sys
import subprocess
import click
import time


class Config(object):
    """
    Global config object which holds all data from .docker.ini
    and manipulates it.
    """
    def __init__(self):
        # parse the config file
        self.config = SafeConfigParser()
        self.name = '.gdocker.ini'
        self.verbose = False

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

    def update_config(self, section, key, value):
        self.config.read(self.name)
        self.config.set(section, key, value)
        if self.verbose:
            click.echo('Verbose: Updated .gdocker.ini [%s=%s]' % (key, value))

    def write_config(self):
        with open(self.name, 'w') as config_file:
            self.config.write(config_file)
            if self.verbose:
                click.echo('Verbose: Config changes written to .gdocker.ini')

    def build_container_cmd(self):
        # read the config file
        self.config.read(self.name)
        # start command
        container_cmd = []
        container_cmd.append("gcloud")
        container_cmd.append("compute")
        # append command options
        container_cmd.append("--project")
        container_cmd.append("" + self.config.get("gcloud", "project_id"))
        container_cmd.append("instances")
        container_cmd.append("create")
        container_cmd.append("gdocker-project")
        container_cmd.append("--zone")
        container_cmd.append("" + self.config.get("gcloud", "zone"))
        container_cmd.append("--machine-type")
        container_cmd.append("" + self.config.get("gcloud", "machine"))
        container_cmd.append("--network")
        container_cmd.append("default")
        container_cmd.append("--image")
        container_cmd.append("" + self.config.get("gcloud", "image"))
        # append meta data
        container_cmd.append("--metadata")
        container_cmd.append("url=" + self.config.get("repo", "url"))
        container_cmd.append("commit=")
        container_cmd.append("start=" + self.config.get("repo", "startup_script"))
        #container_cmd.append("--metadata-from-file")
        #container_cmd.append("google-container-manifest=containers.yaml")
        return container_cmd

    def build_docker_cmd(self):
        # read the config file
        self.config.read(self.name)
        # start command
        docker_cmd = []
        docker_cmd.append("gcloud")
        docker_cmd.append("compute")
        docker_cmd.append("ssh")
        # append command options
        docker_cmd.append("--project")
        docker_cmd.append("" + self.config.get("gcloud", "project_id"))
        docker_cmd.append("--zone")
        docker_cmd.append("" + self.config.get("gcloud", "zone"))
        docker_cmd.append("gdocker-project")
        docker_cmd.append("--command")
        docker_cmd.append("sudo docker run -p " + self.config.get("gcloud", "port") +
                          ":1337 -i -t deshibasara/gdocker-nodejs cd /src && ./docker.sh")
        return docker_cmd

    def build_firewall_cmd(self):
        # read the config file
        self.config.read(self.name)
        # start command
        firewall_cmd = []
        firewall_cmd.append("gcloud")
        firewall_cmd.append("compute")
        firewall_cmd.append("firewall-rules")
        firewall_cmd.append("create")
        firewall_cmd.append("allow-container-port")
        # append command options
        firewall_cmd.append("--project")
        firewall_cmd.append("" + self.config.get("gcloud", "project_id"))
        firewall_cmd.append("--description")
        firewall_cmd.append("Incoming container connection allowed")
        firewall_cmd.append("--allow")
        firewall_cmd.append("tcp:" + self.config.get("gcloud", "port"))
        return firewall_cmd

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
@click.option('--gport', default="40000",
              help="Google container port that should be exposed")
@click.argument('repository_url', required=True)
@click.argument('google_project_id', required=True)
@pass_config
def init(config, repository_url, google_project_id, api_version, startup_script, gzone, gmachine, gimage, gport):
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
    config.set_config("gcloud", "port", gport)

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

    # change the api version number
    config.update_config("repo", "api_version", new_api_version)
    config.write_config()

    # get all needed deployment values from the config
    container_cmd = config.build_container_cmd()

    # start the vm
    deploy_container_process = subprocess.Popen(container_cmd, stdout=subprocess.PIPE)
    click.echo("======================================================================")
    click.echo("1/6 Deploying Container VM on Google Cloud Platform ...")
    click.echo("======================================================================")
    # block io until the vm is ready & print output
    while deploy_container_process.poll() is None:
        new_line = deploy_container_process.stdout.readline()
        click.echo(new_line)

    firewall_cmd = config.build_firewall_cmd()
    firewall_process = subprocess.Popen(firewall_cmd, stdout=subprocess.PIPE)
    click.echo("======================================================================")
    click.echo("2/6 Opening firewall ports on Container VM ...")
    click.echo("======================================================================")
    # block io until the firewall is ready & print output
    while firewall_process.poll() is None:
        new_line = firewall_process.stdout.readline()
        click.echo(new_line)

    # start our docker image on the vm
    click.echo("======================================================================")
    click.echo("3/6 Deploying Docker Image inside Container VM ...")
    click.echo("======================================================================")
    docker_cmd = config.build_docker_cmd()
    click.echo(docker_cmd)
    # timeout execution, until ssh is ready
    time.sleep(5)
    # execute
    docker_process = subprocess.Popen(docker_cmd, stdout=subprocess.PIPE)
    # block io until the container is ready & print output
    while docker_process.poll() is None:
        new_line = docker_process.stdout.readline()
        click.echo(new_line)