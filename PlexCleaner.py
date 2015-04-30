#!/usr/bin/python
# -*- coding: utf-8 -*-

#PlexCleaner based on PlexAutoDelete by Steven4x4 with modifications from others
#Rewrite done by ngovil21 to make the script more cohesive and updated for Plex Home
#Version 1.1 - Added option dump and load settings from a config file

## Config File ###########################################################
#All settings in the config file will overwrite the settings here
Config = ""       #Location of a config file to load options from, can be specified in the commandline with --config [CONFIG_FILE]

## Global Settings #######################################################
Host = ""                     # IP Address of the Plex Media Server, by default 127.0.0.1 will be used
Port = ""                     # Port of the Plex Media Server, by default 32400 will be used
SectionList = []              # Sections to clean. If empty all sections will be looked at
IgnoreSections = []           # Sections to skip cleaning, for use when SectionList is not specified
LogFile = ""                  # Locaton of log file to save console output

#Use Username/Password or Token for servers with PlexHome
#To generate a proper Token, first put your username and password and run the script with the flag --test.
#The Token will be printed in the console or in the logs.
Username = ""
Password = ""
#  or
Token = ""

#Remote Mapping ##########################################################
# For use with managing a remote Plex Media Server that is locally mounted
# This will replace the prefix of the remote file path with the local mount point.
RemoteMount = ""                #Path on the remote server to the media files
LocalMount = ""                 #Path on the local computer to the media files
##########################################################################

## DEFUALT SETTINGS PER SHOW #############################################
# These are the default actions that are applied to each show.
#
# default_action can be set to 'delete','copy','move', 'keep'
# 'delete' will delete the file from the system
# 'copy' will copy the file to the location given
# 'move' will move the file to the location given
# 'keep' will do nothing to the file
# 'flag' will do nothing to the file, but still keep track of stats
default_action = 'flag'     # 'keep' | 'move' | 'copy' | 'delete' | 'flag'
# plex_delete if set to True will use the Plex API to delete files instead of using system functions
# Useful for remote plex installations
plex_delete = False          # True | False
# similar_files if set to True will try to move/copy/delete files with similar filenames to the media file
# Note: delete_similar will not work with plex_delete
similar_files = True       # True | False
# cleanup_movie_folders if set to True will delete folders in movie section path that are less than a certain
# size in megabytes that is set in minimum_folder_size. This is used to cleanup orphaned movie folders when
# a movie file has been deleted by the script or through Plex. Only scanned sections will be affected.
# CAUTION: If you have Plex libraries that are subdirectories of other libraries, the subdirectory may be deleted!
cleanup_movie_folders = False
# minimum_folder_size is the size in megabytes under which a movie folder will be deleted, set to much less,
# than your smallest movie file. If you keep a large amount of extra feature files, this value may need to be adjusted
minimum_folder_size = 30
# default_episodes will keep a certain number of episodes for a show
# If the number of episodes is greater than the default_episodes, older episodes will be deleted
# unless other criteria such as default_watched, default_onDeck, default_minDays are not met
default_episodes = 0        # Number of episodes to keep
# default_watched if set to False will be disabled. If set to True, only episodes that have been
# watched will be deleted if all other criteria are met
default_watched = True      # True | False
# default_onDeck if set to False will be disabled. If set to True, episodes that are On Deck in Plex
# will not be deleted
default_onDeck = True      # True | False
# default_minDays specifies the minimum number of days to keep an episode. Episdoes added more than
# default_minDays ago will be deleted. If default_watched is True, then days from the last watched date
# will be used
default_minDays = 0         # Minimum number of days to keep
# default_maxDays specifies the maximum number of days to keep an episode. Episodes added more than
# default)maxDays ago will be deleted. If default_watched is True, then days from the last wached date
# will be used
default_maxDays = 60	     # Maximum number of days to keep a file
# default_location specifies the location that episodes will be copied or moved to if the action is such
# make sure this is the path to the directory on the local computer
default_location = ''    # /path/to/file
##########################################################################

## CUSTOMIZED SHOW SETTINGS ##############################################
# Customized Settings for certain shows. Use this to override default settings.
# Only the settings that are being changed need to be given. The setting will match the default settings above
# You can also specify an id instead of the Show Name. The id is the id assigned by Plex to the show
# Ex: 'Show Name':{'episodes':3,'watched':True/False,'minDays':,'action':'copy','location':'/path/to/folder'},
# Make sure each show is separated by a comma
ShowPreferences = {
  "Show 1":{"episodes":3,"watched":True,"minDays":10,"action":"delete","location":"/path/to/folder","onDeck":True,"maxDays":30},
  "Show 2":{"episodes":0,"watched":False,"minDays":10,"action":"delete","location":"/path/to/folder","onDeck":False,"maxDays":30},
  "Show 3":{"action":"keep"},   #This show will skipped
  "End Preferences" : {} # Keep this line
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
    print(msg)
  except:
    print("Cannot print message")

def getToken(user,passw):
  import base64

  if sys.version < '3':
    encode = base64.encodestring('%s:%s' % (user,passw)).replace('\n','')
  else:
    auth = bytes('%s:%s' % (user,passw),'utf-8')
    encode =  base64.b64encode(auth).replace(b'\n',b'')
  URL = ("https://plex.tv/users/sign_in.json")
  headers= {
    'X-Plex-Device-Name' : 'Python',
    'X-Plex-Platform' : platform.system(),
    'X-Plex-Device' : platform.system(),
    'X-Plex-Platform-Version' : platform.release(),
    'X-Plex-Provides' : 'Python',
    'X-Plex-Product' : 'Auto Delete Watched',
    'X-Plex-Client-Identifier' : '10101010101010',
    'X-Plex-Version' : platform.python_version(),
    'Authorization' : b'Basic ' + encode
  }
  try:
    if sys.version < '3':
      req = urllib2.Request(URL,"None",headers)
      response = urllib2.urlopen(req)
      str_response = response.read()
    else:
      import urllib
      req = urllib.request.Request(URL,b"None",headers)
      response = urllib.request.urlopen(req)
      str_response = response.readall().decode('utf-8')
    loaded = json.loads(str_response)
    return loaded['user']['authentication_token']
  except:
    return ""

def dumpSettings(output):
  settings = {
    'Host' : Host,
    'Port' : Port,
    'SectionList' : SectionList,
    'IgnoreSections' : IgnoreSections,
    'LogFile' : LogFile,
    'Token' : Token,
    'Username' : Username,
    'Password' : Password,
    'RemoteMount' : RemoteMount,
    'LocalMount' : LocalMount,
    'plex_delete' : plex_delete,
    'similar_files':similar_files,
    'cleanup_movie_folders' : cleanup_movie_folders,
    'minimum_folder_size' : minimum_folder_size,
    'default_episodes' : default_episodes,
    'default_minDays'  : default_minDays,
    'default_maxDays'  : default_maxDays,
    'default_action'   : default_action,
    'default_watched'  : default_watched,
    'default_location' : default_location,
    'default_onDeck'   : default_onDeck,
    'ShowPreferences' : ShowPreferences
  }
  with open(output,'w') as outfile:
    json.dump(settings,outfile,indent=2,sort_keys=True)

def getURLX(URL):
  req = urllib2.Request(URL,None,{"X-Plex-Token":Token})
  return xml.dom.minidom.parse(urllib2.urlopen(req))


def CheckOnDeck(media_id):
  global OnDeckCount
  InTheDeck = 0
  for DeckVideoNode in deck.getElementsByTagName("Video"):
   if DeckVideoNode.getAttribute("ratingKey") == str(media_id):
    OnDeckCount+=1
    return True
  return False


# Crude method to replace a remote path with a local path. Hopefully python properly takes care of file separators.
def getLocalPath(file):
  if RemoteMount and LocalMount:
    if file.startswith(RemoteMount):
      file = os.path.normpath(file.replace(RemoteMount,LocalMount,1))
  return file


#gets the total size of a file in bytes, recursively searches through folders
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


def performAction(file, action, media_id=0, location=""):
  global DeleteCount, MoveCount, CopyCount, FlaggedCount

  file = getLocalPath(file)

  if test:
    if not os.path.isfile(file):
      log("[NOT FOUND] " + file)
      return False
    log("**[FLAGGED] " + file)
    FlaggedCount+=1
    return True
  elif (action.startswith('d') and plex_delete):
    try:
      URL = ("http://" + Host + ":" + Port + "/library/metadata/" + media_id)
      #print(URL)
      req = urllib2.Request(URL,None,{"X-Plex-Token":Token})
      req.get_method = lambda: 'DELETE'
      ret = urllib2.urlopen(req)
      DeleteCount += 1
      log("**[DELETED] " + file)
      return True
    except Exception as e:
      log("Error deleting file: %s" % e,True)
      return False
  if not os.path.isfile(file):
    log("[NOT FOUND] " + file)
    return False
  if similar_files:
    regex = re.sub("\[","[[]",os.path.splitext(file)[0]) + "*"
    log("Finding files similar to: " + regex)
    filelist = glob.glob(regex)
  else:
    filelist = (file,)
  if action.startswith('c'):
    try:
      for f in filelist:
        shutil.copy(os.path.realpath(file), location)
        log("**[COPIED] " + file)
      CopyCount += 1
      return True
    except Exception as e:
      log ("error copying file: %s" % e,True)
      return False
  elif action.startswith('m'):
    for f in filelist:
      try:
          os.utime(os.path.realpath(f), None)
          shutil.move(os.path.realpath(f), location)
          log("**[MOVED] " + f)
      except Exception as e:
        log ("error moving file: %s" % e)
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
        log("error deleting file: %s" % e,True)
        continue
    DeleteCount += 1
    return True
  else:
    log("[FLAGGED] " + file)
    FlaggedCount+=1
    return True


def getMediaInfo(VideoNode):
  view = VideoNode.getAttribute("viewCount")
  if view == '':
    view = 0
  view = int(view)
  ################################################################
  ###Find number of days between date video was viewed and today
  lastViewedAt      = VideoNode.getAttribute("lastViewedAt")
  if lastViewedAt == '':
    DaysSinceVideoLastViewed = 0
  else:
    d1 = datetime.datetime.today()
    d2 = datetime.datetime.fromtimestamp(float(lastViewedAt))
    DaysSinceVideoLastViewed = (d1 -   d2).days
  ################################################################
  ################################################################
  ###Find number of days between date video was added and today
  addedAt      = VideoNode.getAttribute("addedAt")
  if addedAt == '':
    DaysSinceVideoAdded=0
  else:
    d1 = datetime.datetime.today()
    da2 = datetime.datetime.fromtimestamp(float(addedAt))
    DaysSinceVideoAdded = (d1 -   da2).days
  ################################################################
  MediaNode = VideoNode.getElementsByTagName("Media")
  media_id = VideoNode.getAttribute("ratingKey")
  for Media in MediaNode:
    PartNode = Media.getElementsByTagName("Part")
    for Part in PartNode:
      file = Part.getAttribute("file")
      if sys.version < '3':     #remove HTML quoted characters, only works in python < 3
        file = urllib2.unquote(file.encode('utf-8'))
      else:
        file = urllib2.unquote(file)
  return {'view':view,'DaysSinceVideoAdded':DaysSinceVideoAdded,'DaysSinceVideoLastViewed':DaysSinceVideoLastViewed,'file':file,'media_id':media_id}

#Movies are all listed on one page
def checkMovies(doc):
  global FileCount
  global KeptCount

  for VideoNode in doc.getElementsByTagName("Video"):
    title = VideoNode.getAttribute("title")
    movie_id = VideoNode.getAttribute("ratingKey")
    settings = default_settings.copy()
    for key in ShowPreferences:
      if (key.lower() in title.lower()) or (key == movie_id):
        settings.update(ShowPreferences[key])
        break
    #if action is keep then skip checking
    m = getMediaInfo(VideoNode)
    if settings['watched']:
      if m['DaysSinceVideoLastViewed'] > m['DaysSinceVideoAdded']:
        compareDay=m['DaysSinceVideoAdded']
      else:
        compareDay=m['DaysSinceVideoLastViewed']
      log("%s | Viewed: %d | Days Since Viewed: %d" % (title,m['view'],m['DaysSinceVideoLastViewed']))
      checkedWatched = (m['view']>0)
    else:
      compareDay=m['DaysSinceVideoAdded']
      log("%s | Viewed: %d | Days Since Viewed: %d" % (title,m['view'],m['DaysSinceVideoAdded']))
      checkedWatched=True
    FileCount+=1
    checkDeck=False
    if settings['onDeck']:
      checkDeck = CheckOnDeck(movie_id)
    check = (not settings['action'].startswith('k')) and checkedWatched and (compareDay>=settings['minDays']) and (not checkDeck)
    if check:
      performAction(file=m['file'],action=settings['action'],media_id=movie_id,location=settings['location'])
    else:
      log('[Keeping] ' + m['file'])
      KeptCount+=1
    log("")
  if cleanup_movie_folders:
    cleanUpFolders(Section,30)


#Cleans up orphaned folders in a section that are less than the max_size (in megabytes)
def cleanUpFolders(section,max_size):
  log("Cleaning up orphaned folders less than " + str(max_size) + "MB in Section "+str(section))
  for directory in doc_sections.getElementsByTagName("Directory"):
    if directory.getAttribute("key") == section:
      for location in directory.getElementsByTagName("Location"):
        path = getLocalPath(location.getAttribute("path"))
        if os.path.isdir(path):
          for dir in os.listdir(path):
            dir_path = os.path.join(path,dir)
            size = getTotalSize(dir_path)
            if os.path.isdir(dir_path) and size<max_size*1024*1024:
              try:
                if test:
                  log("**[Flagged]: " + dir_path)
                  log("Size " + str(size) + " bytes")
                  continue
                shutil.rmtree(dir_path)
                log("**[DELETED] " + dir_path)
              except Exception as e:
                log("Unable to delete folder: %s" % e, True)
                continue


#Shows have a season pages that need to be navigated
def checkShow(show):
  global KeptCount
  global FileCount
  #Parse all of the episode information from the season pages
  episodes = {}
  settings = default_settings.copy()
  media_container = show.getElementsByTagName("MediaContainer")[0]
  show_id = media_container.getAttribute('key')
  show_name = media_container.getAttribute('parentTitle')
  for key in ShowPreferences:
    if (key.lower() in show_name.lower()) or (key == show_id):
      settings.update(ShowPreferences[key])
      break
  #if action is keep then skip checking
  if settings['action'].startswith('k'):                                 #If keeping on show just skip checking
    log("[Keeping] " + show_name)
    log("")
    return
  for DirectoryNode in show.getElementsByTagName("Directory"):           #Each directory is a season
    if not DirectoryNode.getAttribute('type') == "season":
      continue
    season_key = DirectoryNode.getAttribute('key')
    season_num = str(DirectoryNode.getAttribute('index'))                #Directory index refers to the season number
    if season_num.isdigit():
      season_num = ("%02d" % int(season_num))
    season = getURLX("http://" + Host + ":" + Port + season_key)
    for VideoNode in season.getElementsByTagName("Video"):
      episode_num = str(VideoNode.getAttribute('index'))                 #Video index refers to the epiosde number
      if episode_num.isdigit():                                          #Check if numeric index
        episode_num = ("%03d" % int(episode_num))
      if episode_num == "":                                               #if episode_num blank here, then use something else to get order
        episode_num = VideoNode.getAttribute('originallyAvailableAt')
        if episode_num == "":
          episode_num = VideoNode.getAttribute('title')
          if episode_num == "":
            episode_num = VideoNode.getAttribute('addedAt')
      title = VideoNode.getAttribute('title')
      m = getMediaInfo(VideoNode)
      if settings['watched']:
        if m['DaysSinceVideoLastViewed'] > m['DaysSinceVideoAdded']:
          compareDay=m['DaysSinceVideoAdded']
        else:
          compareDay=m['DaysSinceVideoLastViewed']
      else:
        compareDay=m['DaysSinceVideoAdded']
      key = '%sx%s' % (season_num,episode_num)                      #store episode with key based on season numbeer and episode number for sorting
      episodes[key] = {'season':season_num,'episode':episode_num,'title':title,'view':m['view'],'compareDay':compareDay,'file':m['file'],'media_id':m['media_id']}
      FileCount+=1
  count=0
  for key in sorted(episodes):
    ep = episodes[key]
    if settings['watched']:
      log("%s - S%sxE%s - %s | Viewed: %d | Days Since Last Viewed: %d" % (show_name,ep['season'],ep['episode'],ep['title'],ep['view'],ep['compareDay']))
      checkWatched = (ep['view']>0)
    else:
      log("%s - S%sxE%s - %s | Viewed: %d | Days Since Added: %d" % (show_name,ep['season'],ep['episode'],ep['title'],ep['view'],ep['compareDay']))
      checkWatched = True
    if ((len(episodes)-count) > settings['episodes']) or (ep['view'] > settings['maxDays']):                    #if we have more episodes, then check if we can delete the file
      checkDeck=False
      if settings['onDeck']:
        checkDeck = CheckOnDeck(ep['media_id'])
      check = (not settings['action'].startswith('k')) and checkWatched and (ep['compareDay']>=settings['minDays']) and (not checkDeck)
      if check:
        performAction(file=ep['file'],action=settings['action'],media_id=ep['media_id'],location=settings['location'])
      else:
        log('[Keeping] ' + ep['file'])
        KeptCount+=1
    else:
      log('[Keeping] ' + ep['file'])
      KeptCount+=1
    log("")
    count+=1



## Main Script ############################################

#parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--test","-test",help="Run the script in test mode", action="store_true",default=False)
parser.add_argument("--dump","-dump",help="Dump the settings to a configuration file and exit",nargs='?',const="Cleaner.cfg",default=None)
parser.add_argument("--config","-config","--load","-load",help="Load settings from a configuration file and run with settings")
parser.add_argument("--update_config","-update_config",action="store_true",help="Update the config file with new settings from the script and exit")

args = parser.parse_args()

test=args.test

if args.config:
  Config = args.config
#If no config file is provided, check if there is a config file in first the user directory, or the current directory.
if Config=="":
  if os.path.isfile(os.path.join(os.path.expanduser("~"),".plexcleaner")):
    Config = os.path.join(os.path.expanduser("~"),".plexcleaner")
  elif os.path.isfile(".plexcleaner"):
    Config = ".plexcleaner"
  elif os.path.isfile("Cleaner.cfg")
    Config = "Cleaner.cfg"

if args.dump:
  #Output settings to a json config file and exit
  print("Saving settings to " + args.dump)
  dumpSettings(args.dump)
  exit()

if Config and os.path.isfile(Config):
  print("Loading config file: " + Config)
  with open(Config,'r') as infile:
    settings = json.load(infile)
  if settings['Host']: Host = settings['Host']
  if settings['Port']: Port = settings['Port']
  if settings['SectionList']: SectionList = settings['SectionList']
  if settings['IgnoreSections']: IgnoreSections=settings['IgnoreSections']
  if settings['LogFile']: LogFile = settings['LogFile']
  if settings['Token']: Token = settings['Token']
  if settings['Username']: Username = settings['Username']
  if settings['Password']: Password = settings['Password']
  if settings['LocalMount']: LocalMount = settings['LocalMount']
  if settings['RemoteMount']: RemoteMount = settings['RemoteMount']
  if settings['plex_delete']: plex_delete = settings['plex_delete']
  if settings['similar_files']: similar_files = settings['similar_files']
  if settings['cleanup_movie_folders']: cleanup_movie_folders = settings['cleanup_movie_folders']
  if settings['minimum_folder_size']: minimum_folder_size = settings['minimum_folder_size']
  if settings['default_episodes']: default_episodes = settings['default_episodes']
  if settings['default_minDays']: default_minDays = settings['default_minDays']
  if settings['default_maxDays']: default_maxDays = settings['default_maxDays']
  if settings['default_action']: default_action = settings['default_action']
  if settings['default_watched']: default_watched = settings['default_watched']
  if settings['default_location']: default_location=settings['default_location']
  if settings['default_onDeck']: default_onDeck=settings['default_onDeck']
  if settings['ShowPreferences']: ShowPreferences.update(settings['ShowPreferences'])
  if test:
    print(json.dumps(settings,indent=2,sort_keys=True))   #if testing print out the loaded settings in the log

if args.update_config:
  if Config and os.path.isfile(Config)
    print("Updating Config file with current settings")
    dumpSettings(Config)
    exit()
  else:
    print("No config file found! Exiting!")
    exit()

if Host=="":
  Host="127.0.0.1"
if Port=="":
  Port="32400"

LogToFile=False
if not LogFile=="":
  LogToFile=True
  logging.basicConfig(filename=LogFile,filemode='w',level=logging.DEBUG)
  logging.captureWarnings(True)

if Token=="":
  if not Username=="":
    Token = getToken(Username,Password)
    if Token=="":
      log("Error getting token, trying without...",True)
    elif test:
      log("Token: " + Token,True)
      login = True

default_settings = {'episodes' : default_episodes,
                    'minDays'  : default_minDays,
                    'maxDays'  : default_maxDays,
                    'action'   : default_action,
                    'watched'  : default_watched,
                    'location' : default_location,
                    'onDeck'   : default_onDeck
                    }

log("----------------------------------------------------------------------------")
log("                           Detected Settings")
log("----------------------------------------------------------------------------")
log("Host: " + Host)
log("Port: " + Port)

FileCount = 0
DeleteCount = 0
MoveCount = 0
CopyCount = 0
FlaggedCount = 0
OnDeckCount = 0
KeptCount = 0

doc_sections = getURLX("http://" + Host + ":" + Port + "/library/sections/")

if not SectionList:
  for Section in doc_sections.getElementsByTagName("Directory"):
    if Section.getAttribute("key") not in IgnoreSections:
      SectionList.append(Section.getAttribute("key"))

  SectionList.sort(key=int)
  log ("Section List Mode: Auto")
  log ("Operating on sections: "  +  ','.join(str(x) for x in SectionList))
  log ("Skipping Sections: " +   ','.join(str(x) for x in IgnoreSections))

else:
  log ("Section List Mode: User-defined")
  log ("Operating on user-defined sections: "  +  ','.join(str(x) for x in SectionList))

for Section in SectionList:
  Section = str(Section)

  doc = getURLX("http://" + Host + ":" + Port + "/library/sections/" + Section + "/all")
  deck = getURLX("http://" + Host + ":" + Port + "/library/sections/" + Section + "/onDeck")

  SectionName = doc.getElementsByTagName("MediaContainer")[0].getAttribute("title1")
  log("")
  log("--------- Section "+ Section +": " + SectionName + " -----------------------------------")

  type = doc.getElementsByTagName("MediaContainer")[0].getAttribute("viewGroup")
  if type=="movie":
    checkMovies(doc)
  elif type=="show":
    for DirectoryNode in doc.getElementsByTagName("Directory"):
      show_key = DirectoryNode.getAttribute('key')
      checkShow(getURLX("http://" + Host + ":" + Port + show_key))

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
log("")
log("----------------------------------------------------------------------------")
log("----------------------------------------------------------------------------")
