from ConfigParser import SafeConfigParser
from os import path
import sys

import click


class Config(object):
    """
    Global config object which holds all data from .docker.ini
    and manipulates it.
    """
    def __init__(self):
        # parse the config file
        self.config = SafeConfigParser()
        self.verbose = True

    def create_config(self):
        # create a new '.gdocker.ini'
        with open('.gdocker.ini', 'w') as file:
            # read the newly created file and write two sections into it
            self.config.read('.gdocker.ini')
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
        with open('.gdocker.ini', 'w') as config_file:
            self.config.write(config_file)
            if self.verbose:
                click.echo('Verbose: Config changes written to .gdocker.ini')

    def does_exist(self):
        return path.isfile('.gdocker.ini')


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
@click.option('--start_script', default="start.sh",
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
def init(config, repository_url, google_project_id, api_version, start_script,
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
    config.set_config("gcloud", "project_id", google_project_id)
    config.set_config("gcloud", "zone", gzone)
    config.set_config("gcloud", "machine", gmachine)
    config.set_config("gcloud", "image", gimage)
    config.set_config("gcloud", "start_script", start_script)

    # write config
    config.write_config()


@cli.command()
@click.option('--commit',
              help='Define a sha commit-string that will be deployed')
@click.argument('new_api_version', required=True)
@pass_config
def deploy(config):
    """
    Deploys the latest build in your repository to the google cloud engine.
    If a commit was specified, the commit will be deployed.
    """
    # check if there is an existing .docker.ini file
    if not config.does_exist():
        # does not exist, warn and exit
        click.echo("Error: There is no .gdocker.ini existing, initialise it before deployment")
        sys.exit()