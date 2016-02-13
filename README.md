Plex Cleaner

A Script to clean up space on your Plex Media Server!

Automatically delete watched episodes or movies. Lots of customizable options.

To begin make a copy of Cleaner.conf.default and rename it as Cleaner.conf. You can then make edits to the Cleaner.conf file with your own settings. Descriptions of the settings are in the PlexCleaner.py script.

Alternatively you can create a config file by running the script with the option --dump [Path to Config file].

    python PlexCleaner.py --dump "/path/to/config/file"

PlexCleaner will then create a config file at the path specified with example values. You can then make edits to the config file based on your preferences. The formatting is very specific for the config file, if you have difficulty editing it, you can edit the default values in the script and then run the --dump argument to create a properly formatted config file.

By default plex will check in the users home directory for a .plexcleaner file, then in the current directory for a .plexcleaner or Cleaner.conf file. If you stored the config file in another location you will need to load the config file using the --config argument.
To do so you would run PlexCleaner as:

    python PlexCleaner.py --config "/path/to/config/file"

If the script is updated and you need to update your config file without losing your settings you can run PlexCleaner with --update_config argument. This will add any new configuration settings without overwriting any of your settings in the config file.

After you have entered your settings, it is recommended you first run the script with the --test flag. The --test flag will run the script without performing any actions, and flagging files that would be marked for deletion, copying, or moving. Once you have determined that the output is correct, you can run the script without the --test flag. The --test flag will also output the token used to login so you don't have to leave login details in the script.

If you want to support me (does not equal development): <br>
<a href="https://www.paypal.me/ngovil21/1" target=blank><img src=http://imgur.com/WSVZSTW.png alt="Buy Me a Coffee" height=75 width=150 align='center'></a> &nbsp;&nbsp; or &nbsp;&nbsp; <a href="https://www.paypal.me/ngovil21/3" target=blank><img src=http://imgur.com/gnvlm6n.jpg alt="Buy Me a Beer" height=75 width=150 align='center'></a>

