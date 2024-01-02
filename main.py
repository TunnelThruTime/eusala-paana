# paana - a mail scheduler and prompt for the command line interface
# Copyright © 2023 TunnelThruTime
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# breakpoint()
from datetime import datetime
import re, sys, os, configparser
import termios, tty, subprocess
import click, click_completion
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
global hairpin
hairpin = config.get('general', 'hairpin')
click_completion.init()

# [ ] TODO: test if completions work without click_completion, and Jinja2 <01-01-24, TunnelThruTime> #

# removed calendar artifacts to prevent errors

# callable functions / utilities 
def get_user_input():
    """
    get the keyboard (single press) and return its value 
    """
    
    # Unix-based systems
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        return sys.stdin.read(1).lower()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def checkForSender(item):
    """
    returns a string from the item if present and boolean indicative of success.

    :item: TODO
    :returns: TODO

    """
    sender = item.get('sender')

    print(
            type(sender))

    if sender and 'senders' in config.sections():
        if sender in config['senders']:
            userconf = os.path.expanduser(config['senders'][sender])
            if os.path.exists(userconf) and os.path.isfile(userconf):
                return userconf, True
            else:
                error = "File doesn't exist"
                return error, 1
        else:
            error = "nothing in config section"
            return error, 1



def mail_client(item, status, name, timestamp, recipients, subjectbar, debug=False):
    """
    opens a mail client with subprocess and returns boolean from client

    :reminder: TODO
    :debug: TODO
    :returns: TODO

    """
    if debug:
        console.rule('mail_client function d-bug3r')
        console.print( f'[white]status: {status}[/white]\n' +
                      f'[white]recipients: {recipients}[/white]\n' +
                      f'[grey]name: {name}[/grey]\n' +
                      f'[grey]subjectbar: {subjectbar}[/grey]\n' 
                      )
    if recipients and subjectbar:
        with open('/tmp/paana_header_file.md', 'w') as tmpfl:
            tmpfl.write(f'# content created with paana cli, {timestamp}')
        recipients_str = ','.join(recipients)
        sender = item.get('sender')
        confstring, conftrue = checkForSender(item)
        if conftrue:
            try:
                subprocess.run(["neomutt", "-e", f"source {confstring}",
                               "-s", f"{subjectbar}", "-i", os.path.abspath(tmpfl.name), "--", f"{recipients}"], check=True)
                # neomutt command executed successfully
                message_sent = True
                return True
            except subprocess.CalledProcessError as e:
                # neomutt command returned a non-zero exit code
                message_sent = False
                return False
        else:
            try:
                subprocess.run(["neomutt", "-s", f"{subjectbar}", "-i", os.path.abspath(tmpfl.name), "--", f"{recipients}"], check=True)
                # neomutt command executed successfully
                message_sent = True
                return True
            except subprocess.CalledProcessError as e:
                # neomutt command returned a non-zero exit code
                message_sent = False
                return False

        print("Message sent?", message_sent)
    else:
        print("No recipients, or subject bar")
# Bulk / main code
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

@click.command()
@click.option('--picklefile', type=str, default=repoconfig)
@click.option('--debug', is_flag=True, default=False)
def sift(picklefile, debug):
    """

    :debug: TODO
    :returns: TODO

    """
    # breakpoint()
    dataset = config.get('general', 'hairpin')
    comb = config.get('general', 'comb')
    koyomi = handler.KoyomiManager(picklefile)
    container = koyomi.load_from_pickle(debug=False)
    # run update status loop from koyomi manager
    container[dataset] = koyomi.update_status(container[dataset], verbosity=1, update_last_modified=True)
    # iterate through reminders
    for rmdrs_ind, rmdrs in enumerate(container[dataset]):
        if isinstance(rmdrs, dict):
            status, name, timestamp, recipients = rmdrs.get('status'), rmdrs.get('name'), rmdrs.get('timestamp'), rmdrs.get('recipients')
            subjectbar = rmdrs.get('email_subject_bar')
            if isinstance(status, str) and status.lower() == 'pending':
                console.print( f'({name} [italic]is[/italic] {status}) Open email client? (Yy/Nn)\n' )
                r = get_user_input()
                if r == 'y':
                    message_sent = mail_client(rmdrs, status, name, timestamp, recipients, subjectbar, debug=debug)
                    print(type(message_sent))
                    if isinstance(message_sent, bool) and message_sent is True:
                        print("message sent successfully attempting to alter dataset ...")
                        container[dataset][rmdrs_ind]['status'] = 'completed'
                        container[dataset][rmdrs_ind]['completed'] = True
                        if isinstance(container[dataset][rmdrs_ind], dict):
                            container[comb].append( container[dataset][rmdrs_ind] )
                            container[dataset].remove( container[dataset][rmdrs_ind] )
                        print(f"status set to: [italic red]{container[dataset][rmdrs_ind]['status']}[/italic red]")
                    else:
                        print("message_sent is not a boolean")
    if isinstance(container[dataset], list) and isinstance(container[comb], list):
        koyomi.save_to_pickle(container[dataset], hairpin, destructive=True)
        koyomi.save_to_pickle(container[comb], comb, destructive=True)
    else:
        console.print( f'Error: [yellow]Mismatched data types[/yellow]\n' )







# cli.add_command(debug)
cli.add_command(sift)
cli.add_command(handler.add)
cli.add_command(handler.show)
cli.add_command(handler.rm)
cli.add_command(handler.crop)

if __name__ == '__main__':
    cli()
