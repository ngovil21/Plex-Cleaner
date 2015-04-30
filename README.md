Plex Cleaner

A Script to clean up space on your Plex Media Server!

Automatically delete watched episodes or movies. Lots of customizable options.

There are many options that can be edited in the script. To create a config file run the script with the option --dump [Path to Config file].

    python PlexCleaner.py --dump "/path/to/config/file"

PlexCleaner will then create a config file at the path specified with example values. You can then make edits to the config file based on your preferences.
The formatting is very specific for the config file, if you have difficulty editing it, you can edit the default values in the script and then run the --dump argument to create a properly formatted config file.

By default plex will check in the users home directory for a .plexcleaner file then in the current directory for a .plexcleaner or Cleaner.conf file. If you stored the config file in another location you will need to load the config file using the --config argument.
To do so you would run PlexCleaner as:

    python PlexCleaner.py --config "/path/to/config/file"

If the script is updated and you need to update your config file without losing your settings you can run PlexCleaner with --update_config argument. This will add any new configuration settings without overwriting any of your settings in the config file.

After you have entered your settings, it is recommended you first run the script with the --test flag. The --test flag will run the script without performing any actions, and flagging files that would be marked for deletion, copying, or moving. Once you have determined that the output is correct, you can run the script without the --test flag. The --test flag will also output the token used to login so you don't have to leave login details in the script.