import sys
import re
from collections import OrderedDict

if sys.version < '3':           #use specific types based on python version
    basestring = basestring
else:
    basestring = str

# Recursive method to try and get object types from a string value
# Parses for lists, boolean, int, float, strings
def parseobject(s):
    s = s.strip()
    if re.match('".*"', s) or re.match("\'.*\'", s):  # If surrounded by quotes, return the string without quotes
        return s[1:-1]
    if s.startswith('[') and s.endswith(']'):  # Handle lists
        l = []
        cont = s[1:-1].split(",")
        for v in cont:  # parse objects in between [] separated by commas
            v = v.strip()
            if v == "":
                if len(cont) == 1:  # if empty object, skip
                    continue
            l.append(parseobject(v))  # parse for the type of object and add to list
        return l
    elif s.lower() == 'true':  # if the string is 'true' assume boolean true, string "true" can be handled with "" above
        return True
    elif s.lower() == 'false':  # if the string is 'false' assume boolean false
        return False
    elif s.isdigit():  # if the string is all digits, return an int
        return int(s)
    elif re.match("\d*\.\d*", s) and len(s) > 1:  # if there is one decimal and only digits before or after, return float
        return float(s)
    else:  # if none of the above return a string
        return s


# Returns the indent of the string
def getindent(s):
    s = s.expandtabs(4)
    return len(s) - len(s.lstrip())


# Loads a tabbed key:value config file, indentations create sub-dicts
# Returns a dict with key:value pairs
# ordered will use an OrderedDict, else a built-in dict will be used
def loads(cstring, ordered=False):

    def parselines(lines):  # method to parse multiple lines, used recursively to create a dictionary
        if ordered:
            d = OrderedDict({})  # if ordered set to true, use an ordered dictionary
        else:
            d = {}
        i = 0
        while i < len(lines):  # iterate through lines
            line = lines[i]  # get the current line
            indent = getindent(line)  # get the indent of the current line, count spaces/tabs
            if "#" in line:  # if # is in the line, remove everything after it; for commenting
                line = re.sub('#.*', '', line)
            spl = line.split("=", 1)  # split the line at '=', denotes key/value pairs (split only the first one)
            key = spl[0].strip()  # key will be he first element
            if key.endswith(":"):  # remove end colon off key, defines a nested dictionary
                key = key[:-1].strip()
            if key.startswith('"') or key.startswith("'"):  # remove starting quote
                key = key[1:]
            if key.endswith('"') or key.endswith("'"):  # remove end quote
                key = key[:-1]
            if key == "":  # if the key is empty, then we have an empty line, go to the next line
                i += 1
                continue
            if len(spl) > 1:  # if there is more than one element, we have a key/value pair
                d[key] = parseobject(spl[1])  # parse the value object and place in dict
                i += 1  # go to the next line
                continue
            else:  # there was no value, we are going to process a nested dict
                # j = i + 1
                i += 1
                dlines = []
                while i < len(lines) and getindent(lines[i]) > indent:  # get all lines that have are indented more to create a nested dict
                    dlines.append(lines[i])
                    i += 1
                d[key] = parselines(dlines)  # parse the nested dict lines and place it as the value to the current key
                i -= 1  # loop went one too far, so backtrack one
            i += 1  # go to the next line
        return d  # return the dict

    cstring = cstring.expandtabs(4)  # expand tabs to be 4 spaces
    return parselines(cstring.splitlines())  # recursively parse the lines, split by line break


# Opens a file and parses it with loads
# Returns a dict with key:value pairs
def load(infile, ordered=False):
    with open(infile, 'r') as infile:
        return loads(infile.read(), ordered)


# Returns a string representation of the dictionary data, which can be converted back using loads
# Inputs: data = dict to print, sorted = sort keys, indent = number of spaces to use for sub-dicts
#         start is the starting indent, used recursively in the script, shouldn't be provided
# Returns a string

def dumps(data, sort=False, indent=4, start=0):
    st = ""
    for key in data:
        value = data[key]       #use intermediate variable so we don't modify actual dict value
        if isinstance(value, dict):  # if data is a dict, then print key with a colon after to denote nested dict follows
            st += start * " " + key + ":" + "\n"
            st += dumps(value, sort, indent, start + indent) + "\n"  # recursively dump the nested dict, indented one more level
        else:
            if isinstance(value, basestring):  # if the value is a string, wrap in quotes
                value = '"' + value + '"'
            st += start * " " + key + " = " + str(value) + "\n"
    return st[0:-1]                                                #return string without the last line break


# Write the output of dumps to a file
def dump(data, outfile, sort=False, indent=4):
    with open(outfile, 'w') as outfile:
        outfile.write(dumps(data, sort, indent))
