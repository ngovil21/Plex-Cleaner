import re
from collections import OrderedDict



# Recursive method to try and get object types from a string value
# Parses for lists, boolean, int, float, strings
def parseobject(s):
    s = s.strip()
    if re.match('".*"', s):         # If surrounded by quotes, return the string without quotes
        return s[1:-1]
    if s.startswith('[') and s.endswith(']'):  # Handle lists
        l = []
        for v in s[1:-1].split(","):            # parse objects in between [] separated by commas
            if v == "":                         # if empty object, skip
                continue
            l.append(parseobject(v))            #parse for the type of object and add to list
        return l
    elif s.lower() == 'true':                   #if the string is 'true' assume boolean true, string "true" can be handled with "" above
        return True
    elif s.lower() == 'false':                  #if the string is 'false' assume boolean false
        return False
    elif s.isdigit():                           #Parse numerical values
        if s.count(".") == 0:                   # if there are no decimals, return int
            return int(s)
        elif s.count(".") == 1:                 # if there is one decimal, return float
            return float(s)
        else:                                   # if there are more than one decimal, return a string (used for versioning
            return s
    else:                                       # if none of the above return a string
        return s

# Returns the indent of the current line
def getindent(s):
    return len(s) - len(s.lstrip())


# Loads a tabbed key:value config file, indentations create sub-dicts
# Returns a dict with key:value pairs
# ordered will use an OrderedDict, else a built-in dict will be used
def loads(cstring, ordered=False):

    def parselines(lines):                         # method to parse multiple lines, used recursively to create a dictionary
        if ordered:
            d = OrderedDict({})                    # if ordered set to true, use an ordered dictionary
        else:
            d = {}
        i = 0
        while i < len(lines):                      # iterate through lines
            line = lines[i]                        # get the current line
            indent = getindent(line)               # get the indent of the current line, count spaces/tabs
            if "#" in line:                        # if # is in the line, remove everything after it; for commenting
                line = re.sub('#.*', '', line)
            spl = line.split("=", 1)               # split the line at '=', denotes key/value pairs (split only the first one)
            key = spl[0].strip()                   #key will be he first element
            if key.endswith(":"):  # remove end colon off keys, used stylistically for dictionaries, but not currently required
                key = key[:-1]
            if key == "":                          # if the key is empty, then we have an empty line, go to the next line
                i += 1
                continue
            if len(spl) > 1 and not spl[1].strip() == "":   # if there is more than one element, we have a key/value pair
                d[key] = parseobject(spl[1])                # parse the value object and place in dictionary
                i += 1                                      # go to the next line
                continue
            else:  # assume sub-dictionary                  # there was no value, we are going to process a subdictionary
                # j = i + 1
                i += 1
                dlines = []
                while i < len(lines) and getindent(lines[i]) > indent:          # get all lines that have are indented more to create a subdictioanry
                    dlines.append(lines[i])
                    i += 1
                d[key] = parselines(dlines)                                     # parse the subdictionary lines and place it as the value to the current key
                i -= 1                                                          # loop went one too far, so backtrack one
            i += 1                                                              # go to the next line
        return d                                                                # return the dictionary

    cstring = cstring.expandtabs(4)                         # expand tabs to be 4 spaces
    # cstring.replace(chr(9), "    ")
    return parselines(cstring.splitlines())                 # recursively parse the lines, split by line break


# Opens a file and parses it with loads
# Returns a dict with key:value pairs
def load(file, ordered=False):
    with open(file, 'r') as infile:
        return loads(infile.read(), ordered)


# Returns a string representation of the dictionary data, which can be converted back using loads
# Inputs: data = dict to print, sorted = sort keys, indent = number of spaces to use for sub-dicts
# Returns a string

def dumps(data, sorted=False, indent=4):
    st = ""
    for key in data:
        if isinstance(data[key], dict):                                  # if data is a dict, then print key with a colon after (not necessary, done for style purposes)
            st += key + ":" + "\n"
            temp = dumps(data[key], sorted, indent).split("\n")          # recursively dump the subdictionary and split the lines
            if not isinstance(temp, list):                               # if there is one element (string), then add the one line with indent
                st = " " * indent + temp + "\n"
            else:                                                        # if there is more than one element, go through the elements adding
                for el in temp:
                    st += " " * indent + el + "\n"
        else:
            st += key + " = " + str(data[key]) + "\n"
    return st[0:-1]


# Write the output of dumps to a file
def dump(data, file, sorted=False, indent=4):
    with open(file, 'w') as outfile:
        outfile.write(dumps(data, sorted, indent))
