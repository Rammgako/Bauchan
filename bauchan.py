#!/usr/bin/python -u
import json
import os
import re
import stat
import struct
import subprocess
import sys
import traceback


def is_interactive():
    return os.getenv('INTERACTIVE', False)


def get_message():
    """
    Read a message from stdin and decode it.
    """
    if is_interactive():
        raw_message = raw_input('IN(json)> ')
        if raw_message == 'quit':
            print('Bye!')
            sys.exit(0)
    else:
        raw_length = sys.stdin.read(4)
        if not raw_length:
            sys.exit(0)
        message_length = struct.unpack('=I', raw_length)[0]
        raw_message = sys.stdin.read(message_length)
    return json.loads(raw_message)


def send_message(message):
    """
    Send an encoded message to stdout.
    """
    if is_interactive():
        print('OUT(json)> %s' % json.dumps(message))
    else:
        encoded_content = json.dumps(message)
        encoded_length = struct.pack('=I', len(encoded_content))
        sys.stdout.write(encoded_length)
        sys.stdout.write(encoded_content)
        sys.stdout.flush()


def read_config():
    with open(os.path.expanduser('~/.bauchan.config.json')) as f:
        return json.load(f)


def is_allowed_value(value):
    """
    >>> is_allowed_value('')
    True
    >>> is_allowed_value('x')
    True
    >>> is_allowed_value('!')
    False
    >>> is_allowed_value('x' * 100)
    True
    >>> is_allowed_value('x' * 101)
    False
    """
    return bool(re.match('^[a-zA-Z0-9.-_]{0,100}$', value))


def write_temp_script(config, message):
    script_path = os.path.expanduser(config['path'])
    with open(os.path.expanduser('~/.bauchan.temp.sh'), 'w') as script_file:
        env = [
            '%s=\'%s\'' % (key, value)
            for key, value in message.get('env', {}).items()
        ]
        args = [
            '\'%s\'' % (value)
            for value in message.get('args', [])
        ]
        script_file.write('#!/bin/bash\n%s %s %s\n' % (
            ' '.join(env),
            script_file,
            ' '.join(args)
        ))
    os.chmod(script_file.name, stat.S_IREAD | stat.S_IEXEC | stat.S_IWRITE)


def notify_bauchand():
    with open(os.path.expanduser('~/.bauchan.pid')) as pid_file:
        pid = int(pid_file.read())
        return subprocess.check_output(['/bin/kill', '-SIGUSR2', str(pid)])


def main():
    """
    Accepts 3 message types:
    1. {"type":"config"} would return the content of the ~/.bauchan.config.json
    2. {"type":"run","env":{"VAR1":"VALUE1", ...}} would write variables into a temporary script
    ~/.bauchan.temp.sh and notify bauchand about that
    :return:
    """
    config = read_config()
    while True:
        try:
            message = get_message()
            message_type = message['type']
            if message_type == 'config':
                output = config
            elif message_type == 'run':
                write_temp_script(config, message)
                output = notify_bauchand()
            else:
                output = 'unsupported message type: %s' % message_type
        except Exception as e:
            estr = traceback.format_exc()
            send_message({
                'error': str(e),
                'trace': estr.split('\n')
            })
        else:
            send_message({'output': output})


if __name__ == '__main__':
    main()
