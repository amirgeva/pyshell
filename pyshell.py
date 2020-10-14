#!/usr/bin/env python3
import sys
import subprocess
import os
import re
from ansi import set_colors

user_vars={}
dbglog=None #open('dbg_pyshell.log','w')

def dbg(x):
    if dbglog:
        dbglog.write('{}\n'.format(x));
        dbglog.flush()

def cwd():
    return os.getcwd()

def curdir():
    return os.path.basename(cwd())

def runcmd(cmd):
    if cmd.startswith('cd ') or cmd=='cd':
        dir=cmd[3:]
        if len(dir)==0:
            dir='~'
        dir=subprocess.check_output(['bash','-c','realpath {}'.format(dir)]).strip()
        try:
            os.chdir(dir)
        except OSError:
            print('No such directory')
        return ''
    else:
        dbg("===: '{}'".format(cmd))
        return os.popen(cmd).read()

def add_escapes(s):
    s=s.replace('\n','\\n')
    s=s.replace('\r','\\r')
    s=s.replace('\t','\\t')
    return s

def process_back_quotes(cmd):
    while True:
        m=re.search('`[^`]+`',cmd)
        if not m:
            break
        sub=runcmd(cmd[m.start(0)+1:m.end(0)-1]).strip()
        sub=add_escapes(sub)
        cmd=cmd[0:m.start(0)]+"'"+sub+"'"+cmd[m.end(0):]
    return cmd

def process_escapes(cmd):
    p=-1
    while True:
        p=cmd.find('\\',p+1)
        if p<0:
            break
        if p<len(cmd)-1:
            c=cmd[p+1]
            if c=='n':
                cmd=cmd[0:p]+'\n'+cmd[p+2:]
            if c == 't':
                cmd = cmd[0:p] + '\t' + cmd[p + 2:]
    return cmd

def run_python_cmd(cmd):
    try:
        exec (cmd, user_vars)
    except AttributeError as e:
        print(e)
    except TypeError as e:
        print(e)
    except IndentationError as e:
        print(e)
    except IndexError as e:
        print(e)


def main():
    done=False
    cont=False
    cmdlines=[]
    home=os.path.expanduser('~')
    while not done:
        prompt=cwd()
        if prompt.startswith(home):
            prompt='~'+prompt[len(home):]
        if cont:
            prompt='...'
        set_colors('blue','black',True)
        sys.stdout.write('{}>'.format(prompt));
        set_colors('green','black',False)
        sys.stdout.flush()
        cmd=sys.stdin.readline().rstrip()
        #cmd=process_escapes(cmd)
        cmd=process_back_quotes(cmd)
        dbg("cmd='{}'".format(cmd))
        if cont:
            if len(cmd)==0:
                run_python_cmd('\n'.join(cmdlines))
                cmdlines=[]
                cont=False
            else:
                cmdlines.append(cmd)
            continue
        if cmd=='exit':
            done=True
        try:
            dbg("Trying '{}' type={}".format(cmd,type(cmd)))
            run_python_cmd(cmd)
        except NameError as e:
            msg=str(e)
            dbg("NameError: '{}'".format(msg))
            res=runcmd(cmd)
            sys.stdout.write(res)
        except SyntaxError as e:
            msg=str(e)
            dbg("SyntaxError: '{}'".format(msg))
            if msg.find('unexpected EOF while parsing')>=0:
                cmdlines = [cmd]
                cont=True
            elif msg.find('invalid syntax')>=0:
                res=runcmd(cmd)
                sys.stdout.write(res)
            else:
                dbg("Unknown: cmd='{}' msg='{}'".format(cmd,msg))

if __name__=='__main__':
    main()
