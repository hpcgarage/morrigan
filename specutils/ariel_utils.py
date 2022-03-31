# This module will parse a command and output a dictionary
# that can be provided to ariel to specify the command you want
# to run. Specify any number of arguments and redirects.

# For now, we will focus on input redirect. Others many be added later

# TODO: support standard file descriptors
# TODO: support env params (assignment node)

import bashlex
def parseAriel (command):

    cmd    = None
    args   = []
    stdin  = None
    stdout = None
    stderr = None
    append = False

    parts = bashlex.parse(command)

    if (len(parts) != 1):
        raise ValueError('Expected to recieve exactly one part from the parser')

    ast = parts[0]

    if (ast.kind != 'command'):
        raise ValueError('The command should not include multiple parts, such as with && or |')

    for part in ast.parts:
        if (part.kind == 'word'):
            if (cmd == None):
                cmd = part.word
            else:
                args.append(part.word)
        elif (part.kind == 'redirect'):
            if (part.type == '<'):
                stdin = part.output.word
            elif (part.type == '>'):
                stdout = part.output.word
                redirect = False
            elif (part.type == '>>'):
                stdout = part.output.word
                append = True
        else:
            start = part.pos[0]
            end = part.pos[1]
            raise ValueError('Unsupported command part: {} ({})'.format(command[start:end], part.kind))


    if (not cmd):
        raise ValueError('No command detected')

    params = {}

    params['executable'] = cmd

    params['appargcount'] = len(args)
    for i in range(len(args)):
        params['apparg{}'.format(i)] = args[i]

    if stdin:
        params['appstdin'] = stdin

    if stdout:
        params['appstdout'] = stdout

    return params

