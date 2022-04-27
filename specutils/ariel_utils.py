# Author: Patrick Lavin
#
# This module will parse a command and output a dictionary
# that can be provided to ariel to specify the command you want
# to run. Specify any number of arguments and redirects.
#
# We do not attempt to support arbitrary bash commands. The goal is to
# support basic commands to ease Ariel configuration.
#
# NOTE: While I/O redirection is not currently supported by Ariel, our hope is that it will be soon.
# NOTE: bashlex is license under GPL v3.0

# Examples:
# parseAriel('./mycommand -n 20')
#  -> {'executable': './mycommand', 'appargcount': 2, 'apparg0': '-n', 'apparg1': '20'}
# parseAriel('./mycommand < infile.txt > outfile.txt 2>> errfile.txt')
# -> {'executable': './mycommand', 'appstdin': 'infile.txt', 'appstdout': 'outfile.txt', 'appstdoutappend': 0, 'appstderr': 'errfile.txt', 'appstderrappend': 1}
# parseAriel('MYENVVAR=20 ./mycommand')
# -> {'executable': './mycommand', 'envparamcount': 1, 'envparamname0': 'MYENVVAR', 'envparamval0': '20'}

# Supported features:
# - Parse command name and options
# - Parse environment variables
# - Redirect stdin from file
# - Redirect stdout/stderr to file
# - Choose overwrite or append for stdout/stderr redirection

import bashlex
def parseAriel (command, cmddir='./'):

    cmd     = None
    args    = []
    envname = []
    envval  = []
    stdin   = None
    stdout  = None
    stderr  = None
    stdoutappend = 0
    stderrappend = 0

    if (cmddir[-1] != '/'):
        cmddir = cmddir + '/'

    parts = bashlex.parse(command)

    if (len(parts) != 1):
        raise ValueError('Expected to recieve exactly one part from the parser')

    ast = parts[0]

    if (ast.kind != 'command'):
        raise ValueError('The command should not include multiple parts, such as with && or |')

    for part in ast.parts:

        # The first word node is the command. Further words are arguments.
        if (part.kind == 'word'):

            if (cmd == None):
                cmd = cmddir + part.word
            else:
                args.append(part.word)

        # Redirect nodes represent I/O redirection operations.
        elif (part.kind == 'redirect'):

            if (part.type == '<'):
                stdin = cmddir + part.output.word

            elif (part.type == '>'):
                if (not part.input or part.input == 1):
                    stdout = part.output.word
                    appendstdout = 0
                elif (part.input == 2):
                    stderr = part.output.word
                    appendstderr = 0
            elif (part.type == '>>'):
                if (not part.input or part.input == 1):
                    stdout = part.output.word
                    appendstdout = 1
                elif (part.input == 2):
                    stderr = part.output.word
                    appendstderr = 1

        # Assignment nodes are environment variables. They must appear at the beginning of a command
        # If a node such as VAR=20 is parsed after a word, it will also be parsed as a word, not an assignment.
        elif (part.kind == 'assignment'):

            split = part.word.split('=')
            if (len(split) != 2):
                raise ValueError('Excepted a length 2 array')
            envname.append(split[0])
            envval.append(split[1])

        # We don't support any other nodes.
        else:
            start = part.pos[0]
            end = part.pos[1]
            raise ValueError('Unsupported command part: {} ({})'.format(command[start:end], part.kind))


    if (not cmd):
        raise ValueError('No command detected')

    # Create the params struct used by Ariel.

    params = {}

    params['executable'] = cmd

    if (len(args) > 0) :
        params['appargcount'] = len(args)
        for i in range(len(args)):
            params['apparg{}'.format(i)] = args[i]

    if (len(envname) > 0) :
        params['envparamcount'] = len(envname)
        for i in range(len(envname)):
            params['envparamname{}'.format(i)] = envname[i]
            params['envparamval{}'.format(i)] = envval[i]

    if stdin:
        params['appstdin'] = stdin

    if stdout:
        params['appstdout'] = stdout
        params['appstdoutappend'] = appendstdout

    if stderr:
        params['appstderr'] = stderr
        params['appstderrappend'] = appendstderr

    return params

