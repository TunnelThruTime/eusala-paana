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

from datetime import datetime
import re, sys, os, configparser
import click, click_completion
import pickle, json
from datetime import datetime, timedelta, date
from rich import print
from rich.console import Console
import pretty_errors
import os, sys, re
import rich, pretty_errors
from apscheduler.schedulers.blocking import BlockingScheduler
click_completion.init()
# removed calendar artifacts to prevent errors


current_script_path = os.path.abspath(__file__)
rel_script_path = os.path.join(os.path.dirname(__file__), '..')
git_root = os.path.abspath(rel_script_path)
global config_file_path
config_file_path = os.path.join(git_root, 'xonf', 'config.ini')
global config
config = configparser.ConfigParser()
config.read(os.path.abspath(config_file_path))
repoconfig = os.path.join(git_root, 'xonf', 'koyomi.db')
console = Console(width=config.getint('console', 'width'))
global hairpin, comb
hairpin, comb = config.get('general', 'hairpin'), config.get('general', 'comb')

def script_access_to_resources():
    """TODO: Docstring for script_access_to_resources.

    :): TODO
    :returns: TODO

    """
    console.rule('Resource paths')
    console.print( f'[white]Message: As seen from file {__file__}[/white]\n' +
                  f'[gray]current script path: {current_script_path}[/gray]\n' +
                  f'[white]git_root_relative: {rel_script_path} [/white]\n' +
                  f'[white]git_root: {git_root}[/white]\n' +

                  f'[white]config_file_path: {config_file_path}[/white]\n' +
                  f'[white][/white]\n'
            )

# script_access_to_resources()

def complete_datetime(ctx, args, incomplete):
    today = date.today()
    completions = []
    for i in range(180):
        dt = today + timedelta(days=i)
        completion = dt.strftime('%Y-%m-%d')
        completion_label = dt.strftime('%A')  # Get the day of the week
        if completion.startswith(incomplete):
            completions.append(completion)
    return completions

class KoyomiManager:
    def __init__(self, picklefile):
        self.picklefile = picklefile
        self.events = []
        self.accompli = []
        self.manager = {
            f'{hairpin}': self.events,
            f'{comb}': self.accompli
        }
        self.timefmts = [
            "%Y-%m-%d",                  # Year, Month, Day
            "%Y-%m-%dT%H:%M:%S%z",       # Year, Month, Day, Hour, Minute, Second, Timezone
            "%Y-%m-%dT%H:%M:%S",         # Year, Month, Day, Hour, Minute, Second
            "%Y-%m-%d %H:%M:%S%z",       # Year, Month, Day, Hour, Minute, Second, Timezone
            "%Y-%m-%d %H:%M:%S"          # Year, Month, Day, Hour, Minute, Second
        ]
    
    def save_to_pickle(self, event_dict, mold, destructive=False, force=False, show_results=False):
        """
        saves entire completed dictionary events to the dictiioanry storage medium 'manager'.
        saving is destructive if add parameter is false: old data is replaced by new data.
        all dicitionaries should be complete before adding them to this list of event dictionaries.
        """
        # TODO: Make save_to_pickle function for micro changes, i.e., for individual dictionaries in the list <28-12-23, Luew Leminkainen> #
        # A micro saver would essentially operate in the micro environment by passing a parameter which
        # is already at the level of the dataset for which yoy would save -- this function is passed the db at the macro level
        # of its entirity.

        try:
            if isinstance(self.manager[mold], (str, dict)) and isinstance(event_dict, (str, dict)) and not destructive:
                print( '[red]Warning: container events variable is not a list![/red]\n' +
                        '[green]found events key value as [purple]\"str, or dict\"[/purple][/green]\n' + 
                       f'[blue]destructive is {destructive}[/blue]\n' +
                      '[green]imported events to be save are [purple]\"as string, or dictionary\"' + "\n" + 
                      '[green]fucntion is not [purple]destructive[/purple] [/green]')
                if force:
                    self.manager[mold] = [self.manager.get(mold)]
                    self.manager[mold].append(event_dict)
                    if show_results:
                        print( '[red]Forcing update![/red]\n' +
                                "Appending done, here is new dictionary:", self.manager)
                    else:
                        print( '[red]Forcing update![/red]\n' +
                                "Appending done, exiting ... ")
            elif isinstance(self.manager[mold], (str, dict)) and isinstance(event_dict, list) and not destructive:
                print('[red]Warning: container events variable is not a list![/red]\n' +
                        '[green]found \"events\" key [purple]value as \"string, or dictionary\" [/purple][/green]\n' + 
                       f'[blue]destructive is {destructive}[/blue]\n' +
                      '[green]imported events to be save are [purple]\"as list\"' + "\n" + 
                      '[green]fucntion is not [purple]destructive[/purple] [/green]')
                if force:
                    self.manager[mold] = [self.manager.get(mold)]
                    self.manager[mold] += event_dict
                    if show_results:
                        print( '[red]Forcing update![/red]\n' +
                                "Appending done, here is new dictionary:", self.manager)
                    else:
                        print( '[red]Forcing update![/red]\n' +
                                "Appending done, exiting ... ")
            elif isinstance(self.manager[mold], list) and isinstance(event_dict, (str, dict)) and not destructive:
                print('[bold][violet]Message: container events variable is a list[/bold][/violet]\n' +
                      '[yellow]Ideal Circumstances within database established[/yellow]\n' +
                        '[green]found events key  value [purple]\"as list\" [/purple][/green]\n' + 
                       f'[blue]destructive is {destructive}[/blue]\n' +
                      '[green]imported evenets to be save are [purple]\"as string, or dictionary\"' + "\n" + 
                      '[green]fucntion is not [purple]destructive[/purple] [/green]')
                self.manager[mold].append(event_dict)
                if show_results:
                    print("Appending done, here is new dictionary:", self.manager)
                else:
                    print("Appending done, exiting ...")
            elif isinstance(self.manager[mold], list) and isinstance(event_dict, list) and not destructive:
                print( '[blue]Warning: Input is NOT a dictionary![/blue]\n' +
                       '[yellow]workflow is continuing![/yellow]\n' +
                        '[green]found events key value [purple]\"as list\"[/purple][/green]\n' + 
                       f'[blue]destructive is {destructive}[/blue]\n' +
                       f'[blue]force is set to {force}[/blue]\n' +
                      '[green]imported evenets to be save are [purple]\"as list\"' + "\n" + 
                      '[green]fucntion is [purple]not destructive[/purple] [/green]')
                self.manager[mold] += event_dict
                if show_results:
                    print("Appending done, here is new dictionary:", self.manager)
                else:
                    print("Appending done, exiting ...")
            
            elif isinstance(event_dict, (str, dict)) and destructive:
                print( '[yellow]Message: input event is NOT a list![/yellow]\n' +
                       '[yellow]If force is set overwriting will continue ...[/yellow]\n' +
                       f'[blue]destructive is {destructive}[/blue]\n' +
                       f'[blue]force is set to {force}[/blue]\n' +
                        '[yellow]imported events to be saved are [red]\"as str, or dictionary\"[/red] rather than list[/yellow]' + 
                      '\n' + '[yellow]save function is set to [red]\"destructive\"[/red] rather than not[/yellow]')
                self.manager[mold] = [event_dict]
                if show_results:
                    print("Appending done, here is new dictionary:", self.manager)
                else:
                    print("Appending done, exiting ...")
            elif isinstance(event_dict, list) and destructive:
                print( '[violet]Message: Ideal conditions established[/violet]\n' +
                       '[blue]input is a list[/blue]\n' +
                        '[yellow]imported events to be saved are [red]\"list\"[/red] rather than list[/yellow]\n' + 
                       f'[blue]destructive is {destructive}[/blue]\n' +
                      '\n' + '[yellow]save function is set to [red]\"destructive\"[/red] rather than not[/yellow]')
                self.manager[mold] = event_dict
                if show_results:
                    print("Appending done, here is new dictionary:", self.manager)
                else:
                    print("Appending done, exiting ...")
            else:
                self.manager[mold].append(event_dict)
                print( '[yellow]Message: No other criteria matched[/yellow]\n' +
                      '[yellow]Running else statement of EventManager.save_to_pickle function[/yellow]\n')
                if show_results:
                    print("Appending done, here is new dictionary:", self.manager)
                else:
                    print("Appending done, exiting ...")

        except Exception as e:
            print(f"Something went wrong appending event dictionary to self.manager[{mold}]", str(e))
            if str(e) == "'dict' object has no attribute 'append'":
                print("yea")
        
        # even if you built a micro changing function the overall saving process would still
        # occur in a macro fashion.
        with open(self.picklefile, 'wb') as f:
            pickle.dump(self.manager, f)

    def load_from_pickle(self, exjson=False, debug=True):
        """
        loads from pickle, filling the self.manager

        now has, export json, parameter.
        """
        try:
            with open(self.picklefile, 'rb') as f:
                self.manager = pickle.load(f)
                if debug:
                    print("[blue]Loaded manager dictionary from the pickle: [/blue]", self.manager)
                if exjson:
                    jamison = json.dumps(self.manager)
                    return jamison
                else:
                    return self.manager
        except Exception as e:
            print("Something went wrong, ", str(e))


    def complete_datetime(self, datetime_str):
        formats = [
            "%Y-%m-%d",                  # Year, Month, Day
            "%Y-%m-%dT%H:%M:%S%z",       # Year, Month, Day, Hour, Minute, Second, Timezone
            "%Y-%m-%dT%H:%M:%S",         # Year, Month, Day, Hour, Minute, Second
            "%Y-%m-%d %H:%M:%S%z",       # Year, Month, Day, Hour, Minute, Second, Timezone
            "%Y-%m-%d %H:%M:%S"          # Year, Month, Day, Hour, Minute, Second
        ]
        
        for fmt in self.timefmts:
            try:
                dt = datetime.strptime(datetime_str, fmt)
                return dt.isoformat()
            except ValueError:
                pass
        
        raise ValueError("Invalid datetime format")

    def validate_datetime_string(self, datetime_str):
        if type(datetime_str) is not str:
            datetime_str = str(datetime_str)
        try:
            datetime_obj = datetime.fromisoformat(datetime_str)
            if datetime_obj.tzinfo is None:
                print("Warning: No timezone stamp found in the datetime string.")
        except ValueError:
            print("Error: Invalid datetime string.")



    def weight_datetime_strings(self, begin, end):
        """TODO: Docstring for weight_datetime_strings.

        :dt_start: TODO
        :dt_end: TODO
        :returns: TODO
        """
        try:
            begin_dt = datetime.fromisoformat(begin)
            end_dt = datetime.fromisoformat(end)
        except ValueError as e:
            sys.exit("Invalid datetime format: " + str(e))

        # Check if end datetime is before begin datetime
        if end_dt < begin_dt:
            sys.exit("End datetime cannot be before begin datetime")




    def update_status(self, manager, verbosity=0, debug=False, update_last_modified=False):
        """
        loads the parameter manager at the list level, where self.manager is 'list[dict]'.
        uses iteration for list to evaluate ellapsed timestamps and update their status value.


        please note that this is one level down from the root, where the whole structure
        from the root is 'dict{list[dict]}'.
        evaluation of datetime timestamp against current datetime timestamp
        and if datetime timestamp isn't upcoming switches the status value to 'pending'
        if update_last_modified is True, update the 'last_modified' value to the current datetime timestamp
        in the format of ISO 8601 (YYYY-MM-DDTHH:MM:SStz)
        """
        # breakpoint()
        current_date = datetime.now().date()
        current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
        
        if isinstance(manager, list):
            for item in manager:
                timestamp = item.get('timestamp')
                status = item.get('status')
                stampdtobj = datetime.strptime(timestamp, self.timefmts[2])
            
                if timestamp is not None and isinstance(stampdtobj, datetime) and item['status'] == 'queued':
                    if debug:
                        console.rule("update_status")
                        print("timestamp is not none, stampdtobj is datetime object, and itme status is queued")
                    if stampdtobj.date() <= current_date:
                        if verbosity >= 1:
                            console.print(f'Found queued item that is due')
                        item['status'] = 'pending'
            
                        if update_last_modified:
                            item['last_modified'] = current_timestamp
                        
        return manager

    def check_pickle_file(self, picklefile, debug=True):
        """TODO: Docstring for check_pickle_file.

        :picklefile: TODO
        :returns: TODO

        """
        if not os.path.exists(picklefile):
            # Prompt the user to create the pickle file
            create_file = input("Pickle file doesn't exist. Do you want to create it? (yes/no): ")
            if create_file.lower() == 'yes':
                # Create the pickle file or perform any desired actions
                with open(picklefile, 'wb') as f:
                    # Perform any necessary operations on the file
                    pass
            else:
                # Handle the case where the user doesn't want to create the pickle file
                pass
        else:
            if debug:
                print("[blue]Pickle file exists[/blue]")


@click.group()
def cli():
    pass

@cli.command()
@click.argument('name', type=str)
@click.argument('timestamp', type=str, shell_complete=complete_datetime)
@click.option('--picklefile', type=str, default=repoconfig)
@click.option('--description', type=str, default=None)
@click.option('--uid', type=str, default=None)
@click.option('--subject', '-s', type=str, default=None, help="include subject bar string")
@click.option('--sender', '-S', type=str, default=None, help="send from separate account")
@click.option('--created', type=str, default=None)
@click.option('--last_modified', type=str, default=None)
@click.option('--recipients', '-r', type=str, default=None)
@click.option('--categories', type=list, default=None)
@click.option('--status', type=click.Choice(['queued', 'pending', 'completed'], case_sensitive=False), default='queued')
@click.option('--organizer', type=str, default=None)
@click.option('--classification', type=str, default=None)
@click.option('--force', type=bool, is_flag=True, help='ensures that datafile data is overwritten')
@click.option('--verbose_alarms', is_flag=True, default=False, help="verbosity in alarms set within each event")
@click.option('--show', is_flag=True, default=False, help="print new updated dictionary to stdout")
def add(picklefile, name, timestamp, uid, description, subject, sender, created, last_modified, 
        recipients, categories, status, organizer, classification,
        force, verbose_alarms, show, completed=False):
    """
    add reminders to the dataset 
    """
    manager = KoyomiManager(picklefile)
    manager.check_pickle_file(picklefile)
    stamp = manager.complete_datetime(timestamp)
    manager.validate_datetime_string(stamp)

    current_datetime = datetime.now()
    created = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    try:
        manager.load_from_pickle(debug=False)
    except Exception as e:
        print("raised exception")
        print("An error occured, ", str(e))
    event_dict = {
        'name': name,
        'timestamp': stamp,
        'uid': uid,
        'sender': sender,
        'description': description,
        'email_subject_bar': subject,
        'created': created,
        'last_modified': last_modified,
        'recipients': recipients,
        'categories': categories,
        'status': status,
        'classification': classification,
        'completed': completed
    }

    manager.save_to_pickle(event_dict, hairpin, destructive=False, force=force, show_results=show)
    click_completion.main(args=([name, timestamp]))

@cli.command()
@click.option('--picklefile', type=str, default=repoconfig)
@click.option('--total', is_flag=True, default=False, help="print number of events in list")
@click.option('--pending', is_flag=True, default=False, help="print number of events in list")
@click.option('--completed', is_flag=True, default=False, help="print number of events in list")
@click.option('--queued', is_flag=True, default=False, help="print number of events in list")
@click.option('--enum', is_flag=True, default=False, help="print enumerated reminders")
@click.option('--json', is_flag=True, default=False, help="tells py to export json format")
def show(picklefile, total, pending, queued, completed, enum, json):
    """
    list the contents of pickle file, if specified list dictionaries of list object that
    contain key key pair values.
    """
    manager = KoyomiManager(picklefile)
    if json:
        container = manager.load_from_pickle(exjson=True, debug=False)
    else:
        container = manager.load_from_pickle(debug=False)
    # for event_dict in manager.events:
        # print("Name:", event_dict.get('name'))
        # print("Begin:", event_dict.get('begin'))
        # print("End:", event_dict.get('end'))
    if total:
        print(len(container[hairpin]))
        sys.exit(0)
    if pending:
        for meta in container[hairpin]:
            if meta.get('status') == 'pending':
                print(meta)
    elif queued:
        for meta in container[hairpin]:
            if meta.get('status') == 'queued':
                print(meta)
    elif completed:
        for meta in container[comb]:
            if meta.get('status') == 'completed':
                print(meta)
    elif enum:
        for i, meta in enumerate(container[hairpin]):
            print(i, meta)
    else:
        print(container)


@cli.command(context_settings={"ignore_unknown_options": True})
@click.option('--picklefile', type=str, default=repoconfig)
@click.option('--debug', is_flag=True, default=False, help='print out debug values')
@click.option('--verbose', is_flag=True, default=False, help='print out initial container')
@click.option('--show', is_flag=True, default=False, help='print out results to be saved')
@click.option('--dry', is_flag=True)
@click.argument('pointer', nargs=-1)
def crop(pointer, debug, verbose, dry, picklefile, show):
    """
    crop events from pickle
    """
    manager = KoyomiManager(picklefile)
    container = manager.load_from_pickle(debug=False)
    if verbose:
        print(container[hairpin])

    for tg in pointer:
        print("[blue]string in iteration is:[/blue] ", str(tg))

        if ':' in tg:
            start, end = tg.split(':')
            start = int(start) if start else None
            end = int(end) if end else None
            receiver = container[hairpin][start:end]
        else:
            receiver = container[hairpin][int(tg)]

    if debug:
        console.rule('Crop Debugger')
        console.print("[blue]pointer is [/blue]", type(pointer), justify='right')
        console.print('Length of pointer is: ', len(pointer), justify='right')
        console.print(f"Is container[{hairpin}] a list: ", isinstance(container[hairpin], list), justify='right')
        console.print("Is container a dict: ", isinstance(container, dict), "\n\n", justify='right')

    if show:
        print(receiver)
    if dry:
        sys.exit()
    else:
        container[hairpin] = receiver
        manager.save_to_pickle(container[hairpin], hairpin, destructive=True)

@cli.command(context_settings={"ignore_unknown_options": True})
@click.option('--picklefile', type=str, default=repoconfig)
@click.option('--debug', is_flag=True, default=True)
@click.option('--verbose', is_flag=True)
@click.option('--dry', is_flag=True)
@click.option('--show', is_flag=True, default=False, help="print new updated dictionary to stdout")
@click.option('--span_dbug', is_flag=True, default=False, help="print span class debugger")
@click.argument('pointer', nargs=1)
def rm(pointer, debug, verbose, dry, picklefile, show, span_dbug):
    """
    remove events from pickle using argument pointer as a value.
    If the argument contains a ':' character the character before and after
    the ':' character work as a range for which to remove from the pickle items.
    If the argument contains a ',' character the digits after this character
    will be interpreted as the 'step' value in the pythonic range builtin.
    """
    manager = KoyomiManager(picklefile)
    container = manager.load_from_pickle(debug=False)
    zeit = SpanResolver(container, debug=span_dbug)
    if verbose:
        print(container[hairpin])
    if debug:
        print("[blue]pointer is [/blue]", type(pointer))
        print(len(pointer))
    
    new_events = []  # New list to hold the filtered events
    # the 'if statement' below causes bug for input without colon
    # TODO: if statment below cause bug for input without colon <27-12-23, tunnelthrutime> #
    
    char_pagination = int(len(re.findall(':', pointer)))
    if char_pagination == 1:
        pnter = int(pointer.replace(':', ''))
    elif char_pagination == 0:
        pnter = int(pointer)
    else:
        error_message = "Error: More than one colon is not supported"
        sys.exit(error_message)  # Exit with error message
    
    for index, event in enumerate(container[hairpin]):
        # print("    [yellow]Start: Beginning Loop: -->> [/yellow]")
        dzund = zeit.is_within_slice(index, pointer)
        gzung = int(index) not in [ pnter ]
        # print(f" for index, {index}, and event, {event['name']}")
        # Check if the index is in the pointer or within a slice range
        if int(index) not in [pnter] and not zeit.is_within_slice(index, pointer):
            console.rule(f"Loop for Index {index}")
            print( f'Message: [green]index {index} [blue]Ok[/blue] index not in pointer range[/green]\n' +
                  f'[yellow]    ---->> Appending to list ...[/yellow]\n' +
                   f'[green underline]zeit.is_within_slice is {dzund}[/green underline]\n' +
                  f'[green]within pointer is {gzung}[/green]\n' +
            f"[bold]Loop[/bold]: [green]index {index} is not in pointer and zeit is false[/green]\n\n")
            new_events.append(event)
        else:
            console.rule("section")
            print( f'Message: [green][red]X[/red] Index {index} [dim]found in pointer range![/dim] -->> [red]REMOVING[/red] [/green]\n' +
                  f'[yellow]    ---->> Removing from list ...[/yellow]\n' +
                   f'[green underline]zeit.is_within_slice is {dzund}[/green underline]\n' +
                  f'[green]within pointer is {gzung}[/green]\n' +
                  '[green italic]removing from dataset[/green italic]\n\n' 

                  )
    
    if verbose:
        print(new_events)
    
    if dry:
        sys.exit()
    else:
        container[hairpin] = new_events
        print("is [red]container[/red] a list: ", isinstance(container[hairpin], type(list)))
        manager.save_to_pickle(container[hairpin], hairpin, destructive=True, show_results=show)

class SpanResolver:
    def __init__(self, substrate, debug=False):
        self.substrate = substrate
        self.debug = debug
        
    def is_within_slice(self, index, pointer):
        if self.debug:
            console.rule(f'Debug for {index}')
            console.print(f"within function 'is_within_slice', or {__name__}", justify='center'
                          )
            console.print("pointer is: ", type(pointer), justify='center'
                          )
            console.print(pointer, justify='center'
                          )

        if self.debug:
            m = re.match(r'(\d+)?', pointer)
            print( f'[blue italic]here is the first matching group for pattern (\d+)?[/blue italic]\n' +
                    str(m.group(1)))
        start, stop, step = self.parse_slice(pointer)
        # if start is None:
            # start = 0
        # if stop is None:
            # stop = len(self.substrate[hairpin])
        indices = range(start, stop, step)
        if self.debug:
            print( f'[violet]Indices: {indices}[/violet]\n')
        if index in indices:
            if self.debug:
                console.print(f"[white]function is_within_slice returned true[/white]\n" + 
                      f'[yellow]meaning it should be removed ...[/yellow]\n\n', justify='right' 

                      )
            return True
        else:
            if self.debug:
                console.print(f"[white]function is_within_slice returned false[/white]\n"  +
                      f'[yellow]meaning it should be appended to the new list ...[/yellow]\n\n', justify='right' 
                      )
            return False
            
    @staticmethod
    def is_first_colon(string):
        if re.match(r'^:', string):
            return True
        return False
        
    @staticmethod
    def count_character(string, character):
        count = len(re.findall(character, string))
        return count
        
    def parse_slice(self, slice_str):
        slice_str = str(slice_str)
        if self.debug:
            print("pointer passed to parse_slice function")
            print("[cyan]within parse_slice[/cyan]") 
            print('slice_str is a: ', type(slice_str))
            print(slice_str)
        if self.is_first_colon(slice_str):
            if self.count_character(slice_str, ':') == 3:
                m = re.match(r':(\d+)?:(\d+)?:(\d+)?', slice_str)
                start = 0
                # below I've bumped up the grouping numbers so as to match the regex grouping as
                # I see them at the moment
                stop = int(m.group(1)) if m.group(1) else None
                step = int(m.group(2)) if m.group(2) else 1

            elif self.count_character(slice_str, ':') == 2:
                m = re.match(r':(\d+)?:(\d+)?', slice_str)
                start = 0
                stop = int(m.group(1)) if m.group(1) is not None else None
                step = int(m.group(2)) if m.group(2) else 1

            elif self.count_character(slice_str, ':') == 1:
                m = re.match(r':(\d+)?', slice_str)
                start = 0
                stop = int(m.group(1)) if m.group(1) is not None else None
                step = 1

            elif self.count_character(slice_str, ':') == 0:
                m = re.match(r'(\d+)', slice_str)
                start, stop = int(m.group(1)), None
                step = 1

        else: # else in 'if statement' of parse_slice function
            # in the case where the arg desont' start with the colon
            x = re.match(r'(\d+)', slice_str)
            start = int(x.group(1))
            stop = len(self.substrate[hairpin])
            step = 1
            if start > stop:
                error_message = "Error: Failed to parse slice, Start greater than Stop"
                sys.exit(error_message)  # Exit with error message
            if self.debug:
                m = re.match(r'(\d+)?', slice_str)
                print( f'[blue italic]here is the first matching group for pattern (\d+)?[/blue italic]\n' +
                        m.group(1))
            if self.count_character(slice_str, ':') == 3:
                m = re.match(r'(\d+)?:(\d+)?:(\d+)?', slice_str)
                start = int(m.group(1)) if m.group(1) is not None else None
                stop = int(m.group(2)) if m.group(2) else m.group(1)
                step = int(m.group(3)) if m.group(3) else 1
            elif self.count_character(slice_str, ':') == 2:
                m = re.match(r'(\d+)?:(\d+)?', slice_str)
                start = int(m.group(1)) if m.group(1) is not None else None
                stop = int(m.group(2)) if m.group(2) else m.group(1)
                step = 1
            elif self.count_character(slice_str, ':') == 1 and re.match(r':$', slice_str):
                m = re.match(r'(\d+)(:)', slice_str)
                start = int(m.group(1)) if m.group(1) is not None else None
                stop = len(self.substrate[hairpin])
                step = 1
            elif self.count_character(slice_str, ':') == 0:
                m = re.match(r'(\d+)', str(slice_str))
                start = int(m.group(1)) if m.group(1) is not None else None
                stop = int(m.group(1)) + 1 if m.group(1) is not None else None
                step = 1

        if self.debug:
            console.print('start is: ' + str(start), justify='right')
            console.print('stop is: ' + str(stop), justify='right')
            console.print('step is: ' + str(step), justify='right')

        return start, stop, step
