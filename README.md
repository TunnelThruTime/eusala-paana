# Introduction

teleprompter is a command line interface created for the purpose of 
simplification of the my own emailing processes. Currently just an egg, 
the embryonic idea of what would work well is layout below.

## Concept

Initially the idea behind this project was to have a prompt from the
terminal to send an email. Of course in order to have this accomplished 
we need an engine that at once will open a prompt, then open your email client
with the appropriate recipients attached to the end.

Essentially we first need a pickle dataset to use to store scheduled tasks, with a 
task name, and id, and a datetime. Then there needs to be a method to compare
datetimes, and if that scheduled datetime is equal to the current date, or that
date has ellapsed open the prompt to ask the terminal if the user would 
like to postpone the scheduled email or sent it off.

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

Notes on the project can be stored here. config.ini file is in the xonf dir within the root 
of the project. this dir was supposed to be called conf, but I kept the xonf typo.

### Changelog

removed calendar artifacts left over from beadroll to ensure functioning with ics module.
