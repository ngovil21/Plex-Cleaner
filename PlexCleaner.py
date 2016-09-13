#!/usr/bin/python
# -*- coding: utf-8 -*-

# PlexCleaner based on PlexAutoDelete by Steven4x4 with modifications from others
# Rewrite done by ngovil21 to make the script more cohesive and updated for Plex Home
# Version 1.1 - Added option dump and load settings from a config file
# Version 1.7 - Added options for Shared Users
# Version 1.8 - Added Profies
# Version 1.9 - Added options for checking watch status for multiple users in Plex Home
# Version 1.91 - Added ability to select section by title, preparation for new config
# Version 1.92 - Add ignored folders
# Version 1.93 - Add ability to chose log file mode.
## Config File ###########################################################
# All settings in the config file will overwrite the settings here
Config = ""  # Location of a config file to load options from, can be specified in the commandline with --config [CONFIG_FILE]

## Global Settings #######################################################
Host = ""  # IP Address of the Plex Media Server, by default 127.0.0.1 will be used
Port = ""  # Port of the Plex Media Server, by default 32400 will be used
SectionList = []  # Sections to clean. If empty all sections will be looked at, the section id should be used here which is the number found be in the url on PlexWeb after /section/[ID]
IgnoreSections = []  # Sections to skip cleaning, for use when Settings['SectionList'] is not specified, the same as SectionList, the section id should be used here
LogFile = ""  # Location of log file to save console output
LogFileMode = "overwrite"  # File Mode for logging, overwrite or append, default is overwrite
trigger_rescan = False  # trigger_rescan will rescan a section if changes are made to it

# Use Username/Password or Token for servers with PlexHome
# To generate a proper Token, first put your username and password and run the script with the flag --test.
# The Token will be printed in the console or in the logs. Tokens are preferred so that you password is not in
# a readable files.
# Shared is for users that you have invited to the server. This will use their watch information. Be careful with
# what the default show settings are because deleting files will be done by the OS. To help map the server for
# Shared users, you can specify the server friendly name or machine identifier.
Username = ""
Password = ""
#  or
Token = ""
Shared = False
DeviceName = ""
# Remote Mapping ##########################################################
# For use with managing a remote Plex Media Server that is locally mounted
# This will replace the prefix of the remote file path with the local mount point.
RemoteMount = ""  # Path on the remote server to the media files
LocalMount = ""  # Path on the local computer to the media files
##########################################################################

## DEFAULT SETTINGS PER SHOW #############################################
# These are the default actions that are applied to each show.
#
# default_action can be set to 'delete','copy','move', 'keep'
# 'delete' will delete the file from the system
# 'copy' will copy the file to the location given
# 'move' will move the file to the location given
# 'keep' will do nothing to the file
# 'flag' will do nothing to the file, but still keep track of stats
default_action = 'flag'  # 'keep' | 'move' | 'copy' | 'delete' | 'flag'
# plex_delete if set to True will use the Plex API to delete files instead of using system functions
# Useful for remote plex installations
plex_delete = False  # True | False
# similar_files if set to True will try to move/copy/delete files with similar file names to the media file
# Note: delete_similar will not work with plex_delete
similar_files = True  # True | False
# cleanup_movie_folders if set to True will delete folders in movie section path that are less than a certain
# size in megabytes that is set in minimum_folder_size. This is used to cleanup orphaned movie folders when
# a movie file has been deleted by the script or through Plex. Only scanned sections will be affected.
# CAUTION: If you have Plex libraries that are in subdirectories of other libraries, the subdirectory may be deleted!
cleanup_movie_folders = False
# minimum_folder_size is the size in megabytes under which a movie folder will be deleted, set to much less,
# than your smallest movie file. If you keep a large amount of extra feature files, this value may need to be adjusted
minimum_folder_size = 30
# default_episodes will keep a certain number of episodes for a show
# If the number of episodes is greater than the default_episodes, older episodes will be deleted
# unless other criteria such as default_watched, default_onDeck, default_minDays are not met
default_episodes = 0  # Number of episodes to keep
# default_watched if set to False will be disabled. If set to True, only episodes that have been
# watched will be deleted if all other criteria are met
default_watched = True  # True | False
# default_onDeck if set to False will be disabled. If set to True, episodes that are On Deck in Plex
# will not be deleted
default_onDeck = True  # True | False
# default_minDays specifies the minimum number of days to keep an episode. Episodes added more than
# default_minDays ago will be deleted. If default_watched is True, then days from the last watched date
# will be used
default_minDays = 0  # Minimum number of days to keep
# default_maxDays specifies the maximum number of days to keep an episode. Episodes added more than
# default)maxDays ago will be deleted. If default_watched is True, then days from the last watched date
# will be used
default_maxDays = 60  # Maximum number of days to keep an episode
# default_location specifies the location that episodes will be copied or moved to if the action is such
# make sure this is the path to the directory on the local computer
default_location = ''  # /path/to/file
# default_homeUsers specifies the home users that the script will try to check watch status of in Plex Home
# This will check if all users in the list have watched a show. Separate each user with a comma
# You may use 'all' for the home Users and the script will check watch status of all the users in the Plex Home (Including Guest account if enabled)
# It is probably better to list the users explicitly
default_homeUsers = ''  # 'Bob,Joe,Will'
# if set to anything > 0, videos with watch progress greater than this will be considered watched
default_progressAsWatched = 0  # Progress percentage to consider video as watched
# list of folders to ignore for processing
default_ignoreFolders = []  # Files that are under any of these folders on the Plex Server will not be processed
##########################################################################

## CUSTOMIZED SHOW SETTINGS ##############################################
# Customized Settings for certain shows. Use this to override default settings.
# Only the settings that are being changed need to be given. The setting will match the default settings above
# You can also specify an id instead of the Show Name. The id is the id assigned by Plex to the show
# Ex: 'Show Name':{'episodes':3,'watched':True/False,'minDays':,'action':'copy','location':'/path/to/folder','homeUsers':'Billy,Bob,Joe'},
# Make sure each show is separated by a comma. Use this for TV shows
ShowPreferences = {
    "Show 1": {"episodes": 3, "watched": True, "minDays": 10, "action": "delete", "location": "/path/to/folder",
               "onDeck": True, "maxDays": 30, "homeUsers": 'Bob,Joe,Will'},
    "Show 2": {"episodes": 0, "watched": False, "minDays": 10, "action": "delete", "location": "/path/to/folder",
               "onDeck": False, "maxDays": 30},
    "Show 3": {"action": "keep"},  # This show will skipped
    "Show Preferences": {}  # Keep this line
}
# Movie specific settings, settings you would like to apply to movie sections only. These settings will override the default
# settings set above. Change the default value here or in the config file. Use this for Movie Libraries.
MoviePreferences = {
    # 'watched': default_watched,  # Delete only watched episodes
    # 'minDays': default_minDays,  # Minimum number of days to keep
    # 'action': default_action,  # Action to perform on movie files (delete/move/copy)
    # 'location': default_location,  # Location to keep movie files
    # 'onDeck': default_onDeck  # Do not delete move if on deck
}

# Profiles allow for customized settings based on Plex Collections. This allows managing of common settings using the Plex Web interface.
# First set the Profile here, then add the TV show to the collection in Plex.
Profiles = {
    "Profile 1": {"episodes": 3, "watched": True, "minDays": 10, "action": "delete", "location": "/path/to/folder",
                  "onDeck": True, "maxDays": 30, 'homeUsers': ''}
}
##########################################################################

## DO NOT EDIT BELOW THIS LINE ###########################################
import os
import xml.dom.minidom
import platform
import re
import shutil
import datetime
import glob
import sys
import logging
import json
import argparse
from collections import OrderedDict
import time
import uuid

try:
    import configparser as ConfigParser
except:
    import ConfigParser

CONFIG_VERSION = 1.93
client_id = uuid.uuid1()
home_user_tokens = {}
machine_client_identifier = ''
debug_mode = False
try:
    import urllib.request as urllib2
except:
    import urllib2


def log(msg, debug=False):
    try:
        if LogToFile:
            if debug:
                logging.debug(msg)
            else:
                logging.info(msg)
    except:
        print("Error logging message")
    try:
        print(msg.encode('ascii', 'replace').decode())
    except:
        print("Cannot print message")


def getToken(user, passw):
    import base64

    if sys.version < '3':
        encode = base64.encodestring('%s:%s' % (user, passw)).replace('\n', '')
    else:
        auth = bytes('%s:%s' % (user, passw), 'utf-8')
        encode = base64.b64encode(auth).replace(b'\n', b'')
    URL = "https://plex.tv/users/sign_in.json"
    headers = {
        'X-Plex-Device-Name': 'Python',
        'X-Plex-Username': user,
        'X-Plex-Platform': platform.system(),
        'X-Plex-Device': platform.system(),
        'X-Plex-Platform-Version': platform.release(),
        'X-Plex-Provides': 'Python',
        'X-Plex-Product': 'PlexCleaner',
        'X-Plex-Client-Identifier': '10101010101010',
        'X-Plex-Version': platform.python_version(),
        'Authorization': b'Basic ' + encode
    }
    try:
        if sys.version < '3':
            req = urllib2.Request(URL, "None", headers)
            response = urllib2.urlopen(req)
            str_response = response.read()
        else:
            import urllib
            req = urllib.request.Request(URL, b"None", headers)
            response = urllib.request.urlopen(req)
            str_response = response.readall().decode('utf-8')

        loaded = json.loads(str_response)
        return loaded['user']['authentication_token']
    except Exception as e:
        if debug_mode:
            log("Error getting Token: %s" % e, True)
        return ""


# For Shared users, get the Access Token for the server, get the https url as well
def getAccessToken(token):
    resources = getURLX("https://plex.tv/api/resources?includeHttps=1", token=token)
    if not resources:
        return ""
    devices = resources.getElementsByTagName("Device")
    for device in devices:
        if len(devices) == 1 or machine_client_identifier == device.getAttribute("clientIdentifier") or \
                (Settings['DeviceName'] and (
                        Settings['DeviceName'].lower() in device.getAttribute('name').lower() or Settings[
                    'DeviceName'].lower() in device.getAttribute('clientIdentifier').lower())):
            access_token = device.getAttribute('accessToken')
            if not access_token:
                return ""
            return access_token
        connections = device.getElementsByTagName("Connection")
        for connection in connections:
            if connection.getAttribute('address') == Settings['Host']:
                access_token = device.getAttribute("accessToken")
                if not access_token:
                    return ""
                uri = connection.getAttribute('uri')
                match = re.compile("(http[s]?:\/\/.*?):(\d*)").match(uri)
                if match:
                    Settings['Host'] = match.group(1)
                    Settings['Port'] = match.group(2)
                return access_token
    return ""


def getPlexHomeUserTokens():
    homeUsers = getURLX("https://plex.tv/api/home/users")
    user_tokens = {}
    if homeUsers:
        # print(homeUsers.toprettyxml())
        user_tokens = {}
        for user in homeUsers.getElementsByTagName("User"):
            user_id = user.getAttribute("id")
            switch_page = getURLX("https://plex.tv/api/home/users/" + user_id + "/switch",
                                  data=b'')  # Empty byte data to send a 'POST'
            if switch_page:
                user_element = switch_page.getElementsByTagName('user')[0]
                username = user_element.getAttribute("title").lower()
                home_token = user_element.getAttribute('authenticationToken')
                if home_token:
                    user_tokens[username] = getAccessToken(home_token)
        return user_tokens
    else:
        print("Cannot load page!")
        return {}


# Load Settings from json into an OrderedDict, with defaults
def LoadSettings(opts):
    s = OrderedDict()
    s['Host'] = opts.get('Host', Host)
    s['Port'] = opts.get('Port', Port)
    s['SectionList'] = opts.get('SectionList', SectionList)
    s['IgnoreSections'] = opts.get('IgnoreSections', IgnoreSections)
    s['LogFile'] = opts.get('LogFile', LogFile)
    s['LogFileMode'] = opts.get('LogFileMode', LogFileMode)
    s['trigger_rescan'] = opts.get('trigger_rescan', trigger_rescan)
    s['Token'] = opts.get('Token', Token)
    s['Username'] = opts.get('Username', Username)
    s['Password'] = opts.get('Password', Password)
    s['Shared'] = opts.get('Shared', Shared)
    s['DeviceName'] = opts.get('DeviceName', DeviceName)
    s['RemoteMount'] = opts.get('RemoteMount', RemoteMount)
    s['LocalMount'] = opts.get('LocalMount', LocalMount)
    s['plex_delete'] = opts.get('plex_delete', plex_delete)
    s['similar_files'] = opts.get('similar_files', similar_files)
    s['cleanup_movie_folders'] = opts.get('cleanup_movie_folders', cleanup_movie_folders)
    s['minimum_folder_size'] = opts.get('minimum_folder_size', minimum_folder_size)
    s['default_episodes'] = opts.get('default_episodes', default_episodes)
    s['default_minDays'] = opts.get('default_minDays', default_minDays)
    s['default_maxDays'] = opts.get('default_maxDays', default_maxDays)
    s['default_action'] = opts.get('default_action', default_action)
    s['default_watched'] = opts.get('default_watched', default_watched)
    s['default_progressAsWatched'] = opts.get('default_progressAsWatched', default_progressAsWatched)
    s['default_location'] = opts.get('default_location', default_location)
    s['default_onDeck'] = opts.get('default_onDeck', default_onDeck)
    s['default_homeUsers'] = opts.get('default_homeUsers', default_homeUsers)
    s['default_ignoreFolders'] = opts.get('default_ignoreFolders', default_ignoreFolders)
    s['ShowPreferences'] = OrderedDict(sorted(opts.get('ShowPreferences', ShowPreferences).items()))
    s['MoviePreferences'] = OrderedDict(sorted(opts.get('MoviePreferences', MoviePreferences).items()))
    s['Profiles'] = OrderedDict(sorted(opts.get('Profiles', Profiles).items()))
    s['Version'] = opts.get('Version', CONFIG_VERSION)
    return s


def dumpSettings(output):
    # Remove old settings
    if 'End Preferences' in Settings['ShowPreferences']:
        Settings['ShowPreferences'].pop('End Preferences')
    if 'Movie Preferences' in Settings['MoviePreferences']:
        Settings['MoviePreferences'].pop('Movie Preferences')
    Settings['ShowPreferences'] = OrderedDict(sorted(Settings['ShowPreferences'].items()))
    Settings['MoviePreferences'] = OrderedDict(sorted(Settings['MoviePreferences'].items()))
    Settings['Profiles'] = OrderedDict(sorted(Settings['Profiles'].items()))
    Settings['Version'] = CONFIG_VERSION
    with open(output, 'w') as outfile:
        json.dump(Settings, outfile, indent=2)


def getURLX(URL, data=None, parseXML=True, max_tries=3, timeout=1, referer=None, token=None):
    if not token:
        token = Settings['Token']
    if not URL.startswith('http'):
        URL = 'http://' + URL
    for x in range(0, max_tries):
        if x > 0:
            time.sleep(timeout)
        try:
            headers = {
                'X-Plex-Username': Settings['Username'],
                "X-Plex-Token": token,
                'X-Plex-Platform': platform.system(),
                'X-Plex-Device': platform.machine(),
                'X-Plex-Device-Name': 'Python',
                'X-Plex-Platform-Version': platform.release(),
                'X-Plex-Provides': 'controller',
                'X-Plex-Product': 'PlexCleaner',
                'X-Plex-Version': str(CONFIG_VERSION),
                'X-Plex-Client-Identifier': client_id.hex,
                'Accept': 'application/xml'
            }
            if referer:
                headers['Referer'] = referer
            req = urllib2.Request(url=URL, data=data, headers=headers)
            page = urllib2.urlopen(req)
            if page:
                if parseXML:
                    return xml.dom.minidom.parse(page)
                else:
                    return page
        except Exception as e:
            if debug_mode:
                log("Error requesting page: %s" % e, True)
            continue
    return None


# Returns if a file action was performed (move, copy, delete)
def performAction(file, action, media_id=0, location=""):
    global DeleteCount, MoveCount, CopyCount, FlaggedCount

    file = getLocalPath(file)
    action = action.lower()
    if action.startswith('k'):  # Keep file
        return False
    for path in Settings['default_ignoreFolders']:
        if file.startswith(path):
            log("File is in " + path)
            log("[IGNORED] " + file)
            return False
    if test or action.startswith('f'):  # Test file or Flag file
        if not os.path.isfile(file):
            log("[NOT FOUND] " + file)
            return False
        log("**[FLAGGED] " + file)
        FlaggedCount += 1
        return False
    elif action.startswith('d') and Settings['plex_delete']:  # Delete using Plex Web API
        try:
            URL = (Settings['Host'] + ":" + Settings['Port'] + "/library/metadata/" + str(media_id))
            req = urllib2.Request(URL, None, {"X-Plex-Token": Settings['Token']})
            req.get_method = lambda: 'DELETE'
            urllib2.urlopen(req)
            DeleteCount += 1
            log("**[DELETED] " + file)
            return True
        except Exception as e:
            log("Error deleting file: %s" % e, True)
            return False
    if not os.path.isfile(file):
        log("[NOT FOUND] " + file)
        return False
    if similar_files:
        regex = re.sub("\[", "[[]", os.path.splitext(file)[0]) + "*"
        log("Finding files similar to: " + regex)
        filelist = glob.glob(regex)
    else:
        filelist = (file,)
    if action.startswith('c'):
        try:
            for f in filelist:
                shutil.copy(os.path.realpath(f), location)
                log("**[COPIED] " + file)
            CopyCount += 1
            return True
        except Exception as e:
            log("Error copying file: %s" % e, True)
            return False
    elif action.startswith('m'):
        for f in filelist:
            try:
                os.utime(os.path.realpath(f), None)
                shutil.move(os.path.realpath(f), location)
                log("**[MOVED] " + f)
            except Exception as e:
                log("Error moving file: %s" % e, True)
                return False
            if os.path.islink(f):
                os.unlink(f)
        MoveCount += 1
        return True
    elif action.startswith('d'):
        for deleteFile in filelist:
            try:
                os.remove(deleteFile)
                log("**[DELETED] " + deleteFile)
            except Exception as e:
                log("Error deleting file: %s" % e, True)
                continue
        DeleteCount += 1
        return True
    else:
        log("[FLAGGED] " + file)
        FlaggedCount += 1
        return False


def get_input(prompt=""):
    if sys.version < 3:
        return raw_input(prompt)
    else:
        return input(prompt)


def CheckOnDeck(media_id):
    global OnDeckCount
    if not deck:
        return False
    for DeckVideoNode in deck.getElementsByTagName("Video"):
        if DeckVideoNode.getAttribute("ratingKey") == str(media_id):
            OnDeckCount += 1
            return True
    return False


# Crude method to replace a remote path with a local path. Hopefully python properly takes care of file separators.
def getLocalPath(file):
    if Settings['RemoteMount'] and Settings['LocalMount']:
        if file.startswith(Settings['RemoteMount']):
            file = os.path.normpath(file.replace(Settings['RemoteMount'], Settings['LocalMount'], 1))
    return file


# gets the total size of a file in bytes, recursively searches through folders
def getTotalSize(file):
    total_size = os.path.getsize(file)
    if os.path.isdir(file):
        for item in os.listdir(file):
            itempath = os.path.join(file, item)
            if os.path.isfile(itempath):
                total_size += os.path.getsize(itempath)
            elif os.path.isdir(itempath):
                total_size += getTotalSize(itempath)
    return total_size


def getMediaInfo(VideoNode):
    view = VideoNode.getAttribute("viewCount")
    if view == '':
        view = 0
    view = int(view)
    ################################################################
    ###Find number of days between date video was viewed and today
    lastViewedAt = VideoNode.getAttribute("lastViewedAt")
    if lastViewedAt == '':
        DaysSinceVideoLastViewed = 0
    else:
        d1 = datetime.datetime.today()
        d2 = datetime.datetime.fromtimestamp(float(lastViewedAt))
        DaysSinceVideoLastViewed = (d1 - d2).days
    ################################################################
    ################################################################
    ###Find number of days between date video was added and today
    addedAt = VideoNode.getAttribute("addedAt")
    if addedAt == '':
        DaysSinceVideoAdded = 0
    else:
        d1 = datetime.datetime.today()
        da2 = datetime.datetime.fromtimestamp(float(addedAt))
        DaysSinceVideoAdded = (d1 - da2).days
    if VideoNode.hasAttribute('viewOffset') and VideoNode.hasAttribute('duration'):
        progress = int(VideoNode.getAttribute('viewOffset')) * 100 / int(VideoNode.getAttribute('duration'))
    else:
        progress = 0
    ################################################################
    MediaNode = VideoNode.getElementsByTagName("Media")
    media_id = VideoNode.getAttribute("ratingKey")
    for Media in MediaNode:
        PartNode = Media.getElementsByTagName("Part")
        for Part in PartNode:
            file = Part.getAttribute("file")
            if sys.version < '3':  # remove HTML quoted characters, only works in python < 3
                file = urllib2.unquote(file.encode('utf-8'))
            else:
                file = urllib2.unquote(file)
            return {'view': view, 'DaysSinceVideoAdded': DaysSinceVideoAdded,
                    'DaysSinceVideoLastViewed': DaysSinceVideoLastViewed, 'file': file, 'media_id': media_id,
                    'progress': progress}


def checkUsersWatched(users, media_id, progressAsWatched):
    global home_user_tokens
    if not home_user_tokens:
        home_user_tokens = getPlexHomeUserTokens()
    compareDay = -1
    if 'all' in users:
        users = home_user_tokens.keys()
    for u in users:
        if u in home_user_tokens:
            user_media_page = getURLX(Settings['Host'] + ":" + Settings['Port'] + '/library/metadata/' + media_id,
                                      token=home_user_tokens[u])
            if user_media_page:
                video = user_media_page.getElementsByTagName("Video")[0]
                videoProgress = 0
                if video.hasAttribute('viewOffset') and video.hasAttribute('duration'):
                    videoProgress = int(video.getAttribute('viewOffset')) * 100 / int(video.getAttribute('duration'))
                if (video.hasAttribute('viewCount') and int(video.getAttribute('viewCount')) > 0) or (
                                progressAsWatched > 0 and videoProgress > progressAsWatched):
                    lastViewedAt = video.getAttribute('lastViewedAt')
                    if not lastViewedAt or lastViewedAt == '' or lastViewedAt == '0':
                        DaysSinceVideoLastViewed = 0
                    else:
                        d1 = datetime.datetime.today()
                        d2 = datetime.datetime.fromtimestamp(float(lastViewedAt))
                        DaysSinceVideoLastViewed = (d1 - d2).days
                    if compareDay == -1 or DaysSinceVideoLastViewed < compareDay:  # Find the user who has seen the episode last, minimum DSVLW
                        compareDay = DaysSinceVideoLastViewed
                else:  # Video has not been seen by this user, return -1 for unseen
                    if test:
                        log(u + " has not seen the video: " + media_id)
                    return -1
            else:
                print("Not Found!")
                return -1
        else:
            log("Do not have the token for " + u + ". Please check spelling or report error on forums.")
            return -1
    return compareDay


# Movies are all listed on one page
def checkMovies(doc, section):
    global FileCount
    global KeptCount

    changes = 0
    for VideoNode in doc.getElementsByTagName("Video"):
        movie_settings = default_settings.copy()
        movie_settings.update(Settings['MoviePreferences'])
        title = VideoNode.getAttribute("title")
        movie_id = VideoNode.getAttribute("ratingKey")
        m = getMediaInfo(VideoNode)
        onDeck = CheckOnDeck(movie_id)
        collections = VideoNode.getElementsByTagName("Collection")
        for collection in collections:
            collection_tag = collection.getAttribute('tag')
            if collection_tag and collection_tag in Settings['Profiles']:
                movie_settings.update(Settings['Profiles'][collection_tag])
                print("Using profile: " + collection_tag)
        check_users = []
        if movie_settings['homeUsers']:
            check_users = movie_settings['homeUsers'].strip(" ,").lower().split(",")
            for i in range(0, len(check_users)):  # Remove extra spaces and commas
                check_users[i] = check_users[i].strip(", ")
        if movie_settings['watched']:
            if check_users:
                movie_settings['onDeck'] = False
                watchedDays = checkUsersWatched(check_users, m['media_id'], movie_settings['progressAsWatched'])
                if watchedDays == -1:
                    m['view'] = 0
                    compareDay = 0
                else:
                    m['view'] = 1
                    if watchedDays > m['DaysSinceVideoAdded']:
                        compareDay = m['DaysSinceVideoAdded']
                    else:
                        compareDay = watchedDays
            elif m['DaysSinceVideoLastViewed'] > m['DaysSinceVideoAdded']:
                compareDay = m['DaysSinceVideoAdded']
            else:
                compareDay = m['DaysSinceVideoLastViewed']
            log("%s | Viewed: %d | Days Since Viewed: %d | On Deck: %s" % (
                title, m['view'], m['DaysSinceVideoLastViewed'], onDeck))
            checkedWatched = (m['view'] > 0 or (0 < movie_settings['progressAsWatched'] < m['progress']))
        else:
            compareDay = m['DaysSinceVideoAdded']
            log("%s | Viewed: %d | Days Since Viewed: %d | On Deck: %s" % (
                title, m['view'], m['DaysSinceVideoAdded'], onDeck))
            checkedWatched = True
        FileCount += 1
        checkDeck = False
        if movie_settings['onDeck']:
            checkDeck = onDeck
        check = (not movie_settings['action'].startswith('k')) and checkedWatched and (
            compareDay >= movie_settings['minDays']) and (not checkDeck)
        if check:
            if performAction(file=m['file'], action=movie_settings['action'], media_id=movie_id,
                             location=movie_settings['location']):
                changes += 1
        else:
            log('[Keeping] ' + m['file'])
            KeptCount += 1
        log("")
    if Settings.get('cleanup_movie_folders', False):
        log("Cleaning up orphaned folders less than " + str(minimum_folder_size) + "MB in Section " + section)
        cleanUpFolders(section, minimum_folder_size)
    return changes


# Cleans up orphaned folders in a section that are less than the max_size (in megabytes)
def cleanUpFolders(section, max_size):
    for directory in doc_sections.getElementsByTagName("Directory"):
        if directory.getAttribute("key") == section:
            for location in directory.getElementsByTagName("Location"):
                ignore_folder = False
                for f in Settings['default_ignoreFolders']:
                    if location.getAttribute("path").startswith(f):
                        ignore_folder = True
                if ignore_folder:
                    continue
                path = getLocalPath(location.getAttribute("path"))
                if os.path.isdir(path):
                    for folder in os.listdir(path):
                        dir_path = os.path.join(path, folder)
                        if os.path.isdir(dir_path):
                            if len(
                                    folder) == 1:  # If folder name length is one assume videos are categorized alphabetically, search subdirectories
                                subfolders = os.listdir(dir_path)
                            else:
                                subfolders = (" ",)
                            for subfolder in subfolders:
                                subfolder_path = os.path.join(path, folder, subfolder).strip()
                                if os.path.exists(os.path.join(subfolder_path,
                                                               '.nodelete')):  # Do not delete folders that have .nodelete in them
                                    continue
                                size = getTotalSize(subfolder_path)
                                ignore_folder = False
                                for f in Settings['default_ignoreFolders']:
                                    if subfolder_path.startswith(f):
                                        ignore_folder = True
                                if ignore_folder:
                                    continue
                                if os.path.isdir(subfolder_path) and size < max_size * 1024 * 1024:

                                    try:
                                        if test:  # or default_action.startswith("f"):
                                            log("**[Flagged]: " + subfolder_path)
                                            log("Size " + str(size) + " bytes")
                                            continue
                                        shutil.rmtree(subfolder_path)
                                        log("**[DELETED] " + subfolder_path)
                                    except Exception as e:
                                        log("Unable to delete folder: %s" % e, True)
                                        continue


# Shows have a season pages that need to be navigated
def checkShow(showDirectory):
    global KeptCount
    global FileCount
    # Parse all of the episode information from the season pages
    show_settings = default_settings.copy()
    show_metadata = getURLX(
        Settings['Host'] + ":" + Settings['Port'] + '/library/metadata/' + showDirectory.getAttribute('ratingKey'))
    collections = show_metadata.getElementsByTagName("Collection")
    for collection in collections:
        collection_tag = collection.getAttribute('tag')
        if collection_tag and collection_tag in Settings['Profiles']:
            show_settings.update(Settings['Profiles'][collection_tag])
            print("Using profile: " + collection_tag)
    show = getURLX(Settings['Host'] + ":" + Settings['Port'] + showDirectory.getAttribute('key'))
    if not show:  # Check if show page is None or empty
        log("Failed to load show page. Skipping...")
        return 0
    media_container = show.getElementsByTagName("MediaContainer")[0]
    show_id = media_container.getAttribute('key')
    show_name = media_container.getAttribute('parentTitle')
    for key in Settings['ShowPreferences']:
        if (key.lower() in show_name.lower()) or (key == show_id):
            show_settings.update(Settings['ShowPreferences'][key])
            break
    # if action is keep then skip checking
    if show_settings['action'].startswith('k'):  # If keeping on show just skip checking
        log("[Keeping] " + show_name)
        log("")
        return 0
    check_users = []
    if show_settings['homeUsers']:
        check_users = show_settings['homeUsers'].strip(" ,").lower().split(",")
        for k in range(0, len(check_users)):  # Remove extra spaces and commas
            check_users[k] = check_users[k].strip(", ")
    episodes = []
    for SeasonDirectoryNode in show.getElementsByTagName("Directory"):  # Each directory is a season
        if not SeasonDirectoryNode.getAttribute('type') == "season":  # Only process Seasons (skips Specials)
            continue
        season_key = SeasonDirectoryNode.getAttribute('key')
        season_num = str(SeasonDirectoryNode.getAttribute('index'))  # Directory index refers to the season number
        if season_num.isdigit():
            season_num = ("%02d" % int(season_num))
        season = getURLX(Settings['Host'] + ":" + Settings['Port'] + season_key)
        if not season:
            continue
        for VideoNode in season.getElementsByTagName("Video"):
            episode_num = str(VideoNode.getAttribute('index'))  # Video index refers to the episode number
            if episode_num.isdigit():  # Check if numeric index
                episode_num = ("%03d" % int(episode_num))
            if episode_num == "":  # if episode_num blank here, then use something else to get order
                episode_num = VideoNode.getAttribute('originallyAvailableAt')
                if episode_num == "":
                    episode_num = VideoNode.getAttribute('title')
                    if episode_num == "":
                        episode_num = VideoNode.getAttribute('addedAt')
            title = VideoNode.getAttribute('title')
            m = getMediaInfo(VideoNode)
            if show_settings['watched']:
                if check_users:
                    show_settings['onDeck'] = False
                    watchedDays = checkUsersWatched(check_users, m['media_id'], show_settings['progressAsWatched'])
                    if watchedDays == -1:
                        m['view'] = 0
                        compareDay = 0
                    else:
                        m['view'] = 1
                        if watchedDays > m['DaysSinceVideoAdded']:
                            compareDay = m['DaysSinceVideoAdded']
                        else:
                            compareDay = watchedDays
                elif m['DaysSinceVideoLastViewed'] > m['DaysSinceVideoAdded']:
                    compareDay = m['DaysSinceVideoAdded']
                else:
                    compareDay = m['DaysSinceVideoLastViewed']
            else:
                compareDay = m['DaysSinceVideoAdded']
            # key = '%sx%s' % (season_num, episode_num)  # store episode with key based on season number and episode number for sorting
            episodes.append({'season': season_num, 'episode': episode_num, 'title': title, 'view': m['view'],
                             'compareDay': compareDay, 'file': m['file'], 'media_id': m['media_id'],
                             'progress': m['progress']})
            FileCount += 1
    count = 0
    changes = 0
    for k in range(0, len(episodes)):
        ep = episodes[k]
        onDeck = CheckOnDeck(ep['media_id'])
        if show_settings['watched']:
            log("%s - S%sxE%s - %s | Viewed: %d | Days Since Last Viewed: %d | On Deck: %s" % (
                show_name, ep['season'], ep['episode'], ep['title'], ep['view'], ep['compareDay'], onDeck))
            checkWatched = (ep['view'] > 0 or (0 < show_settings['progressAsWatched'] < ep['progress']))
        else:
            log("%s - S%sxE%s - %s | Viewed: %d | Days Since Added: %d | On Deck: %s" % (
                show_name, ep['season'], ep['episode'], ep['title'], ep['view'], ep['compareDay'], onDeck))
            checkWatched = True
        if not (not ((len(episodes) - k) > show_settings['episodes']) and not (
                        ep['compareDay'] > show_settings[
                        'maxDays'] > 0)):  # if we have more episodes, then check if we can delete the file
            checkDeck = False
            if show_settings['onDeck']:
                checkDeck = onDeck or (k + 1 < len(episodes) and CheckOnDeck(episodes[k + 1]['media_id']))
                if debug_mode and checkDeck:
                    print("File is on deck, not deleting")
            check = (not show_settings['action'].startswith('k')) and checkWatched and (
                ep['compareDay'] >= show_settings['minDays']) and (not checkDeck)
            if check:
                if performAction(file=ep['file'], action=show_settings['action'], media_id=ep['media_id'],
                                 location=show_settings['location']):
                    changes += 1
            else:
                log('[Keeping] ' + getLocalPath(ep['file']))
                KeptCount += 1
        else:
            log('[Keeping] ' + getLocalPath(ep['file']))
            KeptCount += 1
        log("")
        count += 1
    return changes


## Main Script ############################################

# reload sys to set default encoding to utf-8
reload(sys)
sys.setdefaultencoding("utf-8")

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--test", "-test", help="Run the script in test mode", action="store_true", default=False)
parser.add_argument("--dump", "-dump", help="Dump the settings to a configuration file and exit", nargs='?',
                    const="Cleaner.conf", default=None)
parser.add_argument("--config", "-config", "--load", "-load",
                    help="Load settings from a configuration file and run with settings")
parser.add_argument("--update_config", "-update_config", action="store_true",
                    help="Update the config file with new settings from the script and exit")
parser.add_argument("--debug", "-debug", action="store_true",
                    help="Run script in debug mode to log more error information")
parser.add_argument("--config_edit", "-config_edit", action="store_true",
                    help="Prompts for editing the config from the commandline")

args = parser.parse_args()

test = args.test
debug_mode = args.debug

if args.config:
    Config = args.config
# If no config file is provided, check if there is a config file in first the user directory, or the current directory.
if Config == "":
    if os.path.isfile(os.path.join(os.path.expanduser("~"), ".plexcleaner")):
        Config = os.path.join(os.path.expanduser("~"), ".plexcleaner")
    elif os.path.isfile(os.path.join(sys.path[0], "Cleaner.conf")):
        Config = os.path.join(sys.path[0], "Cleaner.conf")
    elif os.path.isfile(os.path.join(sys.path[0], "Settings.cfg")):
        Config = os.path.join(sys.path[0], "Settings.cfg")
    elif os.path.isfile(".plexcleaner"):
        Config = ".plexcleaner"
    elif os.path.isfile("Cleaner.conf"):
        Config = "Cleaner.conf"

Settings = OrderedDict()

if Config and os.path.isfile(Config):
    print("Loading config file: " + Config)
    with open(Config, 'r') as infile:
        opt_string = infile.read().replace('\n', '')  # read in file removing breaks
        # Escape odd number of backslashes (Windows paths are a problem)
        opt_string = re.sub(r'(?x)(?<!\\)\\(?=(?:\\\\)*(?!\\))', r'\\\\', opt_string)
        options = json.loads(opt_string)
        Settings = LoadSettings(options)
    if ('Version' not in options) or not options['Version'] or (options['Version'] < CONFIG_VERSION):
        print("Old version of config file! Updating...")
        dumpSettings(Config)
else:
    Settings = LoadSettings(Settings)

if args.dump:
    # Output settings to a json config file and exit
    print("Saving settings to " + args.dump)
    dumpSettings(args.dump)
    print("Settings saved. Exiting...")
    exit()

if test:
    print(json.dumps(Settings, indent=2, sort_keys=False))  # if testing print out the loaded settings in the console

if args.update_config:
    if Config:
        # resp = get_input("Edit Settings in console? (y/n)")
        # if resp.lower().startswith("y"):
        #     while True:
        print("Updating Config file with current settings")
        dumpSettings(Config)
        exit()
    else:
        print("No config file found! Exiting!")
        exit()

if Settings['Host'] == "":
    Settings['Host'] = "127.0.0.1"
if Settings['Port'] == "":
    Settings['Port'] = "32400"

if test:
    print(json.dumps(Settings, indent=2))
    print("")

LogToFile = False
if not Settings['LogFile'] == "":
    LogToFile = True
    filemode = "w"
    if Settings.get("LogFileMode").startswith("a"):
        filemode = "a"
    logging.basicConfig(filename=Settings['LogFile'], filemode=filemode, level=logging.DEBUG)
    logging.captureWarnings(True)

log("** Script started " + time.strftime("%m-%d-%Y %I:%M:%S%p"))
log("")

if Settings['Token'] == "":
    if Settings['Username']:
        Settings['Token'] = getToken(Settings['Username'], Settings['Password'])
        if not Settings['Token']:
            log("Error getting token, trying without...", True)
        elif test:
            log("Token: " + Settings['Token'], True)
            login = True

server_check = getURLX(Settings['Host'] + ":" + Settings['Port'] + "/")
if server_check:
    media_container = server_check.getElementsByTagName("MediaContainer")[0]
    if not Settings['DeviceName']:
        Settings['DeviceName'] = media_container.getAttribute("friendlyName")
    if not machine_client_identifier:
        machine_client_identifier = media_container.getAttribute("machineIdentifier")

if Settings['Shared'] and Settings['Token']:
    accessToken = getAccessToken(Settings['Token'])
    if accessToken:
        Settings['Token'] = accessToken
        if test:
            log("Access Token: " + Settings['Token'], True)
    else:
        log("Access Token not found or not a shared account")

if not Settings['Host'].startswith("http"):
    Settings['Host'] = "http://" + Settings['Host']

default_settings = {'episodes': Settings['default_episodes'],
                    'minDays': Settings['default_minDays'],
                    'maxDays': Settings['default_maxDays'],
                    'action': Settings['default_action'],
                    'watched': Settings['default_watched'],
                    'progressAsWatched': Settings['default_progressAsWatched'],
                    'location': Settings['default_location'],
                    'onDeck': Settings['default_onDeck'],
                    'homeUsers': Settings['default_homeUsers']
                    }

log("----------------------------------------------------------------------------")
log("                           Detected Settings")
log("----------------------------------------------------------------------------")
log("Host: " + Settings['Host'])
log("Port: " + Settings['Port'])

FileCount = 0
DeleteCount = 0
MoveCount = 0
CopyCount = 0
FlaggedCount = 0
OnDeckCount = 0
KeptCount = 0

doc_sections = getURLX(Settings['Host'] + ":" + Settings['Port'] + "/library/sections/")

if (not Settings['SectionList']) and doc_sections:
    for Section in doc_sections.getElementsByTagName("Directory"):
        if Section.getAttribute("key") not in Settings['IgnoreSections'] and Section.getAttribute("title") not in \
                Settings['IgnoreSections']:
            Settings['SectionList'].append(Section.getAttribute("key"))
elif doc_sections and Settings['SectionList']:  # Replace section names with the proper id(/key)
    for i in range(0, len(Settings['SectionList'])):
        if isinstance(Settings['SectionList'][i], int):  # Skip checking name of integers (these are keys)
            continue
        for Section in doc_sections.getElementsByTagName("Directory"):
            if Section.getAttribute("title") == str(Settings['SectionList'][i]):
                Settings['SectionList'][i] = int(Section.getAttribute("key"))

    Settings['SectionList'].sort()
    # log("Section List Mode: Auto")
    log("Operating on sections: " + ','.join(str(x) for x in Settings['SectionList']))
    log("Skipping Sections: " + ','.join(str(x) for x in Settings['IgnoreSections']))

else:
    log("Section List Mode: User-defined")
    log("Operating on user-defined sections: " + ','.join(str(x) for x in Settings['SectionList']))

RescannedSections = []

for Section in Settings['SectionList']:
    Section = str(Section)

    doc = getURLX(Settings['Host'] + ":" + Settings['Port'] + "/library/sections/" + Section + "/all")
    deck = getURLX(Settings['Host'] + ":" + Settings['Port'] + "/library/sections/" + Section + "/onDeck")

    if not doc:
        log("Failed to load Section %s. Skipping..." % Section)
        continue
    SectionName = doc.getElementsByTagName("MediaContainer")[0].getAttribute("title1")
    log("")
    log("--------- Section " + Section + ": " + SectionName + " -----------------------------------")

    group = doc.getElementsByTagName("MediaContainer")[0].getAttribute("viewGroup")
    changed = 0
    if group == "movie":
        changed = checkMovies(doc, Section)
    elif group == "show":
        for DirectoryNode in doc.getElementsByTagName("Directory"):
            changed += checkShow(DirectoryNode)
    if changed > 0 and Settings['trigger_rescan']:
        log("Triggering rescan...")
        if getURLX(Settings['Host'] + ":" + Settings['Port'] + "/library/sections/" + Section + "/refresh?deep=1",
                   parseXML=False):
            RescannedSections.append(Section)

log("")
log("----------------------------------------------------------------------------")
log("----------------------------------------------------------------------------")
log("                Summary -- Script Completed Successfully")
log("----------------------------------------------------------------------------")
log("")
log("  Total File Count      " + str(FileCount))
log("  Kept Show Files       " + str(KeptCount))
log("  On Deck Files         " + str(OnDeckCount))
log("  Deleted Files         " + str(DeleteCount))
log("  Moved Files           " + str(MoveCount))
log("  Copied Files          " + str(CopyCount))
log("  Flagged Files         " + str(FlaggedCount))
log("  Rescanned Sections    " + ', '.join(str(x) for x in RescannedSections))
log("")
log("----------------------------------------------------------------------------")
log("----------------------------------------------------------------------------")
