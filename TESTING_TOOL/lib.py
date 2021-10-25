from inspect import currentframe, getframeinfo


def get_raw_filename(name):
    for i in range(len(name)-1, -1, -1):
        if name[i] == "/":
            return name[i+1:], name[:i]
    return name, "./"


def to_type(arg, t):
    error_message = "\033[93m" + \
        f"TYPE ERROR! YOU PUT WRONG INPUT in .py.test file!" + "\033[0m"
    if t == "int":
        try:
            return int(arg)
        except ValueError:
            cl = getframeinfo(currentframe())
            say(error_message, "r", cl.lineno)
            exit()
    if t == "str":
        try:
            return str(arg)
        except ValueError:
            cl = getframeinfo(currentframe())
            say(error_message, "r", cl.lineno)
            exit()
    if t == "float":
        try:
            return float(arg)
        except ValueError:
            cl = getframeinfo(currentframe())
            say(error_message, "r", cl.lineno)
            exit()
    if t == "bool":
        try:
            return bool(arg)
        except ValueError:
            cl = getframeinfo(currentframe())
            say(error_message, "r", cl.lineno)
            exit()

    if t == "List[int]" or t == "List[str]" or t == "List[float]" or t == "List[bool]":
        try:
            l = []
            for item in arg:
                if item != "[" and item != "]" and item != ",":
                    # kinda recusrsion
                    l.append(to_type(item, t[5:-1]))
            return l
        except ValueError:
            cl = getframeinfo(currentframe())
            say(error_message, "r", cl.lineno)
            exit()
    cl = getframeinfo(currentframe())
    say("UNKNOWN TYPE!", "r", cl.lineno)
    exit()


def say(text, t, currentline):
    if t == "warn" or t == "yellow" or t == "y":
        color = "\033[93m"
    elif t == "error" or t == "type_error" or t == "red" or t == "r":
        color = "\033[91m"
    elif t == "corr_type" or t == "blue" or t == "b":
        color = "\033[94m"
    elif t == "ok" or t == "green" or t == "g":
        color = "\033[92m"
    else:
        color = ""

    print(color + str(currentline) +
          "\033[0m" + ":" + color + text + "\033[0m")


def get_args_and_results(line, types):
    line = line.split(";")
    types = types.split(";")

    args = []
    results = []
    i = 0

    for arg in line[0].split(":"):
        args.append(to_type(arg, types[i]))
        i += 1

    for res in line[1].split(":"):
        results.append(to_type(res, types[i]))
        i += 1

    return args, results


def py_file_scraping(file_txt):
    functions_in_py = []
    funcs_count = file_txt.count("def")

    i = 0
    while funcs_count != 0:
        func = []
        df = file_txt.index("def", i)
        bracket_open = file_txt.index("(", i)
        bracket_close = file_txt.index(")", i)
        arrow = file_txt.index(">", i)
        colon = file_txt.index(":", arrow)

        func.append(file_txt[df+4:bracket_open])

        args_types = ""
        args = file_txt[bracket_open+1:bracket_close]
        args_colons = args.count(":")
        i = 0
        last_comma_i = -2
        comma_i = -1
        while args_colons != 0:
            args_colon_i = args.index(":", i)
            if last_comma_i != comma_i:
                comma_i = args.index(",", i)
                last_comma_i = comma_i
            else:
                comma_i = len(args)

            args_types += args[args_colon_i+2:comma_i] + ";"

            i = comma_i
            args_colons -= 1

        func.append(args_types + file_txt[arrow+2:colon])
        functions_in_py.append(func)

        i = colon
        funcs_count -= 1

    return functions_in_py


def visualize_input_types(expects):
    for i in range(len(expects)):
        func = expects[i][0]
        line = []
        for arg in expects[i][1]:
            line.append(str(type(arg)).replace(
                "<class '", "").replace("'>", ""))
        for res in expects[i][2]:
            line.append(str(type(res)).replace(
                "<class '", "").replace("'>", ""))

        args = expects[i][1] + expects[i][2]

        cl = getframeinfo(currentframe())
        say(f"{args} are {line}", "b", cl.lineno)
