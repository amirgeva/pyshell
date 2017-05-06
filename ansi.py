import sys

foreground={
    'black':   '\033[30m',
    'red':     '\033[31m',
    'green':   '\033[32m',
    'yellow':  '\033[33m',
    'blue':    '\033[34m',
    'magenta': '\033[35m',
    'cyan':    '\033[36m',
    'white':   '\033[37m'
}

background={
    'black':   '\033[40m',
    'red':     '\033[41m',
    'green':   '\033[42m',
    'yellow':  '\033[43m',
    'blue':    '\033[44m',
    'magenta': '\033[45m',
    'cyan':    '\033[46m',
    'white':   '\033[47m'
}

def set_colors(fg,bg,bold):
    cmd=''
    if fg in foreground:
        cmd=cmd+foreground.get(fg)
    #if bg in background:
    #    cmd=cmd+background.get(bg)
    if bold:
        cmd=cmd+'\033[1m'
    else:
        cmd = cmd + '\033[22m'
    sys.stdout.write(cmd)
