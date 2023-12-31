---
title: NOTES
layout: template
filename: notes.md
---

## Concept

Initially the idea behind this project was to have a prompt from the
terminal to send an email. Of course in order to have this accomplished 
we need an engine that at once will open a prompt, then open your email client
with the appropriate recipients attached to the end.

Essentially we first need:
1. [X]  pickle dataset to use to store scheduled tasks, with a task name, and id, and a datetime. 
2. [X]  Then there needs to be a method to compare
    datetimes, and if that scheduled datetime is equal to the current date, or that
    date has ellapsed open the prompt to ask the terminal if the user would 
    like to postpone the scheduled email or sent it off.
3. [X] pickle dataset to store a 'sender' value, to be used as a 'hook'

In order to do this there needs to be something that intializes the process.


### Processes 

Imported EventManager from beadroll to facilitate a database manager.

It seems like a large portion of what I've written in my beadroll application can be carried over to
the usage of this new program. For instance, the class the manages the database pickle, and 
also the first major command 'add', which utilizes a dictionary which is populated from a series
of options that are passed via the click options into the dicitonary itself.

Of these for the purposes of creating and loading and then removing the urgency of 
the events which I would facilitate, 'status', seems important.

If I use string evaluation, I could in theory, use the strings, 'pending', and 'completed' to the
status key value pair. Alternatively, I could add a boolean value.

It has just occured to me that it would be more advantageous to have the program running in three statices, 
so as to represent a queued position, a pending position and a completed position.
IN that way if the datetime has elapsed the position would switch to pending, and repeated ask the user
if they want to complete the task in pending position. Then once the task has been completed the 
status could change to completed.

### Notes

Notes on the project can be stored here. _'config.ini'_ file is in the xonf dir within the root 
of the project. this dir was supposed to be called conf, but I kept the xonf typo.

Added lines to handler.py that drastically change the makeup of the project. Instead of hardcoding 
a key for the dicitonary storage within the pickle I've decided instead to go to 
the usage of dynamically set values from the config.ini

In the general header this can be configured using the `hairpin = reminder` for instance.
This will be my setting, since this particular program will be built to remind me of email that
need to be set out to campaign for the political advance of careerism. Can't wait for the fall
... of capitalism. 

#### Improvements to the database

It doesn't make much sense to keep those items in the list that have been completed since the rm function
acts by index, and indices. 

1. [X] save items to separate dictionary once they are completed.

#### Inserting json output compatibility

Last night after work and before going to bed I inserted json output functionality for the script.
I did that by adding a boolean parameter inside the class 'KoyomiManager' function 'load_from_pickle'.
then I attached another boolean as a flag to my click decorated function and in the function added
lines that would add or remove the boolean from a line to be executed in the works. The circuit works 
because the user uses a option that set the boolean to true or false, if the option is true it calls 
a line of code that sets a classes' function parameter to true and tells the return value to be called
from a line using the python json module.

#### Notes on the bugs of the show command

It was my ideal to have the output of the show command capable of being parsed using the `jq` command,
however currently there are separate characters being dished out of the command that are U+8000 to U+000F,
and this breaks the functionalkty of commands such as:

```
paana show | jq '.'
```

#### Notes on core functionality

The core function can be divided into two operations, (1.), an operation which retrieves the list of dictionaries and parses the status
for the truth of the pending string within the status variable, and (2.), a secondary operation opening a Yy/Nn
prompt for the user in which Yy will initiate a subprocess containing 'neomutt', or whatever mail chimp
the user decides to use.

This could be dependent on a category within the config.ini file with the header 'mailchimp', or 'pigeon', or
something else along those lines.

Of course this isn't entirely accurate, as there is another step involved before this. That is of course the preliminary
step that is the comparision of datestamps to determine their status. I think however that I've finished this step.

