import re
from collections import OrderedDict



# Recursive method to try and get object types from a string value
def parseobject(s):
    s = s.strip()
    if re.match('".*"', s):
        return s[1:-1]
    if s.startswith('[') and s.endswith(']'):  # Handle lists
        l = []
        for v in s[1:-1].split(","):
            if v == "":
                continue
            l.append(parseobject(v))
        return l
    elif s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False
    elif s.isdigit():
        if s.count(".") == 0:
            return int(s)
        elif s.count(".") == 1:
            return float(s)
        else:
            return s
    else:
        return s


def getindent(s):
    return len(s) - len(s.lstrip())


# Loads a tabbed key:value config file, indentations create sub-dicts
# Returns a dict with key:value pairs
# ordered will use an OrderedDict, else a built-in dict will be used
def loads(cstring, ordered=False):
    def parselines(lines):
        if ordered:
            d = OrderedDict({})
        else:
            d = {}
        i = 0
        while i < len(lines):
            line = lines[i]
            indent = getindent(line)
            if "#" in line:
                line = re.sub('#.*', '', line)
            spl = line.split("=", 1)
            key = spl[0].strip()
            if key.endswith(":"):  # remove end colon off keys that are used for dictionaries, but not required as of now
                key = key[:-1]
            if key == "":
                i += 1
                continue
            if len(spl) > 1 and not spl[1].strip() == "":
                d[key] = parseobject(spl[1])
                i += 1
                continue
            else:  # assume sub-dictionary
                # j = i + 1
                i += 1
                dlines = []
                while i < len(lines) and getindent(lines[i]) > indent:
                    dlines.append(lines[i])
                    i += 1
                d[key] = parselines(dlines)
                i -= 1
            i += 1
        return d

    cstring = cstring.expandtabs(4)
    # cstring.replace(chr(9), "    ")
    return parselines(cstring.splitlines())


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
        if isinstance(data[key], dict):
            st += key + ":" + "\n"
            temp = dumps(data[key], sorted, indent).split("\n")
            if not isinstance(temp, list):
                st = " " * indent + temp + "\n"
            else:
                for el in temp:
                    st += " " * indent + el + "\n"
        else:
            st += key + " = " + str(data[key]) + "\n"
    return st[0:-1]


# Write the output of dumps to a file
def dump(data, file, sorted=False, indent=4):
    with open(file, 'w') as outfile:
        outfile.write(dumps(data, sorted, indent))


        # with open("C:\Users\Nikhil\Documents\GitHub\Plex-Cleaner\Cleaner.conf.default", 'r') as infile:
        # opt_string = infile.read().replace('\n', '')  # read in file removing breaks
        # Escape odd number of backslashes (Windows paths are a problem)
        # opt_string = re.sub(r'(?x)(?<!\\)\\(?=(?:\\\\)*(?!\\))', r'\\\\', opt_string)
        # options = json.loads(opt_string)
        # options =load(infile, True)


options = load("C:\Users\Nikhil\Documents\GitHub\Plex-Cleaner\\notepad_test.txt", True)
print(dumps(options))
