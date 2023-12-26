breakpoint()
from datetime import datetime
import re, sys, os, configparser
import click
import pickle
from datetime import datetime, timedelta
from rich import print
from rich.console import Console
import pretty_errors
import os, sys, re
import rich, pretty_errors
from apscheduler.schedulers.blocking import BlockingScheduler
from lib import handler
from lib import handler

current_script_path = os.path.abspath(__file__)
git_root = os.path.dirname(current_script_path)
global config_file_path
config_file_path = os.path.join(git_root, 'xonf', 'config.ini')
global config
config = configparser.ConfigParser()
config.read(os.path.abspath(config_file_path))
repoconfig = os.path.join(git_root, 'xonf', 'koyomi.db')
console = Console(width=config.getint('console', 'width'))

# removed calendar artifacts to prevent errors

@click.group()
def cli():
    pass

@click.command()
@click.argument('type', required=False)
def debug(type):
    """TODO: Docstring for debug.

    :): TODO
    :returns: TODO

    """
    handler.script_access_to_resources()

cli.add_command(debug)
cli.add_command(handler.add)
cli.add_command(handler.show)
cli.add_command(handler.rm)
cli.add_command(handler.crop)

