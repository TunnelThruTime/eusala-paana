---
title: README
layout: template
filename: README.md
---


# Introduction

![eusela](640px-White_shark_Duane_Raver.png)

The interface, based off the finnish word for prompt, ('paana'), is a command line utility created for the purpose of email scheduling.
the concept lies in producing a prompt, 'paana', asking the user to proceed with a prescheduled email. 
Embryonic, the idea of what would work well is laid out below.

the interface has five commands: add, crop, debug, rm, show, sift. I will take the time to briefly go
over the properties of each command explaining them.


##  add    

the database stores individual reminders and the two main attributes of each reminder are requisite in the add command: timestamp, and 
name. the name attribute is no send out in the emails is only used for the user internally. the timestamp is cached to compare against
the current date as described above.

the subject option, `--subject`, or `-s`, gives you a subject bar for your queued emails, but this can be altered latter when you go to send the emails
within neomutt itself.

the add command is one of two core commands that alter the database, which by default is set to be inside the repository,
however it is possible to use the option `--picklefile` to use another database. You are more than welcome to do this and example 
command has a picklefile option to consistantly alter a secondary database.


##  crop  

the crop command let you remove items from the database outside of a certain range which you supply it. It has certain options
of which the most is important is `--dry` which stops the process before altering the database.

##  rm     

the rm, or remove, command will remove items from the database. This command uses pythonic splicing so that using a number preceeded or followed by
a colon will remove all the entries to or from that entry to end or beginning.

##  show

using this command you can list which items are pending, queued, or completed within the database.
Naturally when a item is added it is added to a reminders list, and its status is set to 'queued', the sift command described 
below will update the status of each item within the list. show has options for displaying each of these categories, 
as well as for enumerating the listes themselves.
   
##  sift

the sift command will compare the current date against the reminders and display a prompt for you if your reminders are pending.
pending reminders will remain pending until you have sent the emails. paana does this by collecting the status exit on the subprocess
initialized in the scripting. once completed the sift command will move the item to the completed list and remove it from the reminders
list.

# Installation

clone the repo, use `python -m venv custenv`, `source custenv/bin/activate', and then install with pip. After this is
done you can follow instructions about the completions below.

add the line `paana sift` to your bashrc or zshrc config file to utilize the prompt, or simply check the database regularly
with that command.


# Configuration

paana has a config.ini file which the interface reads it base configuration from and there are some elements which can 
be altered. 

##### Multiple neomutt accounts, and the 'sender' value

A third 'core' functionality, could lie in the use of a dataset item dictionary key-value pair using sender.
The concept would be to use a value that is searched for within the config.ini section 'sender'. 
The program would match a key within the 'sender' category as opposed to the value. This would allow uses
to write their own key-pair values within the sender section. 

If the value is retrievable then the neomutt send command would be altered as such:
`neomutt -e "source ~/.path/to/accounts/account2" -s 'subjectbar' -i $tmpfl -- $frecipients`

There where the variables \$tmpfl, ('temporary file'), and \$frecipients, ('formated recipients'), 
are a simple representation of what they would be in the shell.

This means that users will need to define the key-values themselves, and by definition it means
a degree of code netting, or work flow netting within the codebase. But this 
functionality is only an addtional feature and excluding the sender value when adding email reminders to
the database is completely operational. 

Defining the values can be achieved as follows, where the value is the absolute path to your configuration
file. <span></span>
```
[senders]

email = ~/.mutt/myprofile/profile.1
pigeon = ~/.mutt/myprofile/profile.2
```
with the above configuration scheduling to send from your second profile can be achieved with `-S pigeon`.

this feature is dependant on the workings of [multi accounts](https://neomutt.org/test-doc/bestpractice/multiprofile), as described on
their website in the page I've linked here. 

##### Different names for the reminder and completed lists

inside the configuration file, and inside the python scripting the two lists, that for completed and that for queued or pending reminders
have different titles. They are 'comb', for things that have been combed out of the reminders, and 'hairpin', for things proped up.
You can alter these values to set new names for the lists themselves. Essentially what this allows is for multiple lists, but although
that is a result of the coding it is outside what I had intented for it. I just thought it was cool to be able to configure the names yourself.

By default the two lists are 'reminders', and 'accompli', but feel free to use them as you like.

### Add commnad options

Do you need a subject bar string. Yes of course, but it
might be a cool idea to have presets for what type of email your writing. Just like it might be best to have differrent
presets for the type of neomutt command you are running. Does it include attachments? 

### Addition notes

paana was written with the click module, and for that reason has some builtin completion copacities. In click pallets version
8.1.x., which is bound to outdated when you come across this project, they state that a completions shell script can be compiled
with, and Ive configurated this to 'paana':

```
_PAANA_COMPLETE=zsh_source paana > _paana
```
at which point you should test your fpath with `echo $fpath`, choose a suitable directory, and move the file there.
If you are having trouble consult the your shell scripting language documentation.

### Furthur Reading

More notes, including my own, on the building process, and its usage can be found on [the notes page](notes.md).

### Changelog

removed calendar artifacts left over from beadroll to ensure functioning with ics module.
