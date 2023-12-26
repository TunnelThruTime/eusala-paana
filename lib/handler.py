

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

class KoyomiManager:
    def __init__(self, picklefile):
        self.picklefile = picklefile
        self.events = []
        self.alarms = []
        self.manager = {
            'events': self.events,
            'alarms': self.alarms
        }
    
    def save_to_pickle(self, event_dict, destructive=False, force=False, show_results=False):
        """
        saves entire completed dictionary events to the dictiioanry storage medium 'manager'.
        saving is destructive if add parameter is false: old data is replaced by new data.
        all dicitionaries should be complete before adding them to this list of event dictionaries.
        """

        try:
            if isinstance(self.manager['events'], (str, dict)) and isinstance(event_dict, (str, dict)) and not destructive:
                print( '[red]Warning: container events variable is not a list![/red]\n' +
                        '[green]found events key value as [purple]\"str, or dict\"[/purple][/green]\n' + 
                       f'[blue]destructive is {destructive}[/blue]\n' +
                      '[green]imported events to be save are [purple]\"as string, or dictionary\"' + "\n" + 
                      '[green]fucntion is not [purple]destructive[/purple] [/green]')
                if force:
                    self.manager['events'] = [self.manager.get('events')]
                    self.manager['events'].append(event_dict)
                    if show_results:
                        print( '[red]Forcing update![/red]\n' +
                                "Appending done, here is new dictionary:", self.manager)
                    else:
                        print( '[red]Forcing update![/red]\n' +
                                "Appending done, exiting ... ")
            elif isinstance(self.manager['events'], (str, dict)) and isinstance(event_dict, list) and not destructive:
                print('[red]Warning: container events variable is not a list![/red]\n' +
                        '[green]found \"events\" key [purple]value as \"string, or dictionary\" [/purple][/green]\n' + 
                       f'[blue]destructive is {destructive}[/blue]\n' +
                      '[green]imported events to be save are [purple]\"as list\"' + "\n" + 
                      '[green]fucntion is not [purple]destructive[/purple] [/green]')
                if force:
                    self.manager['events'] = [self.manager.get('events')]
                    self.manager['events'] += event_dict
                    if show_results:
                        print( '[red]Forcing update![/red]\n' +
                                "Appending done, here is new dictionary:", self.manager)
                    else:
                        print( '[red]Forcing update![/red]\n' +
                                "Appending done, exiting ... ")
            elif isinstance(self.manager['events'], list) and isinstance(event_dict, (str, dict)) and not destructive:
                print('[bold][violet]Message: container events variable is a list[/bold][/violet]\n' +
                      '[yellow]Ideal Circumstances within database established[/yellow]\n' +
                        '[green]found events key  value [purple]\"as list\" [/purple][/green]\n' + 
                       f'[blue]destructive is {destructive}[/blue]\n' +
                      '[green]imported evenets to be save are [purple]\"as string, or dictionary\"' + "\n" + 
                      '[green]fucntion is not [purple]destructive[/purple] [/green]')
                self.manager['events'].append(event_dict)
                if show_results:
                    print("Appending done, here is new dictionary:", self.manager)
                else:
                    print("Appending done, exiting ...")
            elif isinstance(self.manager['events'], list) and isinstance(event_dict, list) and not destructive:
                print( '[blue]Warning: Input is NOT a dictionary![/blue]\n' +
                       '[yellow]workflow is continuing![/yellow]\n' +
                        '[green]found events key value [purple]\"as list\"[/purple][/green]\n' + 
                       f'[blue]destructive is {destructive}[/blue]\n' +
                       f'[blue]force is set to {force}[/blue]\n' +
                      '[green]imported evenets to be save are [purple]\"as list\"' + "\n" + 
                      '[green]fucntion is [purple]not destructive[/purple] [/green]')
                self.manager['events'] += event_dict
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
                self.manager['events'] = [event_dict]
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
                self.manager['events'] = event_dict
                if show_results:
                    print("Appending done, here is new dictionary:", self.manager)
                else:
                    print("Appending done, exiting ...")
            else:
                self.manager['events'].append(event_dict)
                print( '[yellow]Message: No other criteria matched[/yellow]\n' +
                      '[yellow]Running else statement of EventManager.save_to_pickle function[/yellow]\n')
                if show_results:
                    print("Appending done, here is new dictionary:", self.manager)
                else:
                    print("Appending done, exiting ...")

        except Exception as e:
            print("Something went wrong appending event dictionary to self.manager['events']", str(e))
            if str(e) == "'dict' object has no attribute 'append'":
                print("yea")
        
        with open(self.picklefile, 'wb') as f:
            pickle.dump(self.manager, f)

    def load_from_pickle(self, debug=True):
        """
        loads from pickle, filling the self.manager
        """
        try:
            with open(self.picklefile, 'rb') as f:
                self.manager = pickle.load(f)
                if debug:
                    print("[blue]Loaded manager dictionary from the pickle: [/blue]", self.manager)
                return self.manager
        except Exception as e:
            print("Something went wrong, ", str(e))


    def validate_datetime_string(self, datetime_str):
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
@click.argument('timestamp', type=str)
@click.argument('end', required=False, type=str)
@click.option('--picklefile', type=str, default=repoconfig)
@click.option('--duration', type=str, default=None)
@click.option('--uid', type=str, default=None)
@click.option('--description', type=str, default=None)
@click.option('--pending', type=bool, default=True)
@click.option('--created', type=str, default=None)
@click.option('--last_modified', type=str, default=None)
@click.option('--location', type=str, default=None)
@click.option('--url', type=str, default=None)
@click.option('--transparent', type=bool, default=None)
@click.option('--alarms', type=str, default=None, help="Read docstring")
@click.option('--attendees', type=list, default=None)
@click.option('--categories', type=list, default=None)
@click.option('--status', type=str, default='pending')
@click.option('--organizer', type=str, default=None)
@click.option('--geo', type=tuple, default=None)
@click.option('--classification', type=str, default=None)
@click.option('--force', type=bool, is_flag=True, help='ensures that datafile data is overwritten')
@click.option('--verbose_alarms', is_flag=True, default=False, help="verbosity in alarms set within each event")
@click.option('--show', is_flag=True, default=False, help="print new updated dictionary to stdout")
def add(picklefile, name, timestamp, end, duration, uid, description, pending, created, last_modified, location,
        url, transparent, alarms, attendees, recipients, categories, status, organizer, geo, classification,
        force, verbose_alarms, show):
    """
    add reminders to the dataset 
    """
    manager = KoyomiManager(picklefile)
    manager.check_pickle_file(picklefile)
    manager.validate_datetime_string(timestamp)
    manager.validate_datetime_string(end)
    manager.weight_datetime_strings(timestamp, end)
    try:
        manager.load_from_pickle(debug=False)
    except Exception as e:
        print("raised exception")
        print("An error occured, ", str(e))
    event_dict = {
        'name': name,
        'timestamp': timestamp,
        'end': end,
        'duration': duration,
        'uid': uid,
        'description': description,
        'pending': pending,
        'created': created,
        'last_modified': last_modified,
        'location': location,
        'url': url,
        'transparent': transparent,
        'alarms': alarms,
        'attendees': attendees,
        'recipients': recipients,
        'categories': categories,
        'status': status,
        'organizer': organizer,
        'geo': geo,
        'classification': classification
    }

    manager.save_to_pickle(event_dict, destructive=False, force=force, show_results=show)

@cli.command()
@click.option('--picklefile', type=str, default=repoconfig)
@click.option('--total', is_flag=True, default=False, help="print number of events in list")
def show(picklefile, total):
    """
    list the contents of pickle file
    """
    manager = KoyomiManager(picklefile)
    container = manager.load_from_pickle(debug=False)
    # for event_dict in manager.events:
        # print("Name:", event_dict.get('name'))
        # print("Begin:", event_dict.get('begin'))
        # print("End:", event_dict.get('end'))
    if total:
        print(len(container['events']))
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
    manager = EventManager(picklefile)
    container = manager.load_from_pickle(debug=False)
    if verbose:
        print(container['events'])

    for tg in pointer:
        print("[blue]string in iteration is:[/blue] ", str(tg))

        if ':' in tg:
            start, end = tg.split(':')
            start = int(start) if start else None
            end = int(end) if end else None
            receiver = container['events'][start:end]
        else:
            receiver = container['events'][int(tg)]

    if debug:
        console.rule('Crop Debugger')
        console.print("[blue]pointer is [/blue]", type(pointer), justify='right')
        console.print('Length of pointer is: ', len(pointer), justify='right')
        console.print("Is container['events'] a list: ", isinstance(container['events'], list), justify='right')
        console.print("Is container a dict: ", isinstance(container, dict), "\n\n", justify='right')

    if show:
        print(receiver)
    if dry:
        sys.exit()
    else:
        container['events'] = receiver
        manager.save_to_pickle(container['events'], destructive=True)

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
    manager = EventManager(picklefile)
    container = manager.load_from_pickle(debug=False)
    zeit = SpanResolver(container, debug=span_dbug)
    if verbose:
        print(container['events'])
    if debug:
        print("[blue]pointer is [/blue]", type(pointer))
        print(len(pointer))
    
    new_events = []  # New list to hold the filtered events
    if len(re.findall(':', pointer)) == 1:
        pnter = int(pointer.replace(':', ''))
    else:
        error_message = "Error: More than one colon is not supported"
        sys.exit(error_message)  # Exit with error message
    
    for index, event in enumerate(container['events']):
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
        container['events'] = new_events
        print("is [red]container[/red] a list: ", isinstance(container['events'], type(list)))
        manager.save_to_pickle(container['events'], destructive=True, show_results=show)

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
            # stop = len(self.substrate['events'])
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
            stop = len(self.substrate['events'])
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
                stop = len(self.substrate['events'])
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
