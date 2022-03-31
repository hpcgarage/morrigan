# This module will parse a command and output a dictionary
# that can be provided to ariel to specify the command you want
# to run. Specify any number of arguments and redirects.

# For now, we will focus on input redirect. Others many be added later

# TODO: support standard file descriptors
# TODO: support env params (assignment node)

import bashlex
def parseAriel (command):

    cmd     = None
    args    = []
    envname = []
    envval  = []
    stdin   = None
    stdout  = None
    stderr  = None
    stdoutappend = False
    stderrappend = False

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
                if (not part.input or part.input == 1):
                    stdout = part.output.word
                    appendstdout = False
                elif (part.input == 2):
                    stderr = part.output.word
                    appendstderr = False
            elif (part.type == '>>'):
                if (not part.input or part.input == 1):
                    stdout = part.output.word
                    appendstdout = True
                elif (part.input == 2):
                    stderr = part.output.word
                    appendstderr = True

        elif (part.kind == 'assignment'):

            split = part.word.split('=')
            if (len(split) != 2):
                raise ValueError('Excepted a length 2 array')
            envname.append(split[0])
            envval.append(split[1])

        else:
            start = part.pos[0]
            end = part.pos[1]
            raise ValueError('Unsupported command part: {} ({})'.format(command[start:end], part.kind))


    if (not cmd):
        raise ValueError('No command detected')

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
        params['appendstdout'] = appendstdout

    if stderr:
        params['appstderr'] = stderr
        params['appendstderr'] = appendstderr

    return params

