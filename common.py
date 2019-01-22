import logging
import plistlib
import os
import stat


def configure_logging(target: str):
    log_dir = os.path.join(os.path.expanduser('~'), 'Library', 'Logs', 'Bauchan')
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler(os.path.join(log_dir, '%s.log' % target))
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s:%(name)s:%(message)s'))
    logging.root.addHandler(handler)


def write_script(path, content):
    with open(path, 'w') as script_file:
        script_file.write(content)
    os.chmod(script_file.name, stat.S_IREAD | stat.S_IEXEC | stat.S_IWRITE)


class Data(object):
    def __init__(self, application_support_path='~/Library/Application Support/org.example.bauchan'):
        self._path = os.path.expanduser(application_support_path)
        # TODO: Replace Data.plist with .pid file in the Application Support directory
        self._filename = os.path.join(self._path, 'Data.plist')
        os.makedirs(self._path, exist_ok=True)

    def _load(self):
        try:
            with open(self._filename, 'rb') as fp:
                data = plistlib.load(fp, fmt=plistlib.FMT_XML)
        except FileNotFoundError:
            data = {}
        return data

    def _dump(self, data):
        with open(self._filename, 'wb') as fp:
            plistlib.dump(data, fp, fmt=plistlib.FMT_XML)

    def _get(self, key, default):
        data = self._load()
        return data.get(key, default)

    def _set(self, key, value):
        data = self._load()
        data[key] = value
        self._dump(data)

    def _unset(self, key):
        data = self._load()
        if key in data:
            del data[key]
        self._dump(data)

    @property
    def temp_script_path(self) -> str:
        return self._get('TemporaryScriptPath', os.path.join(self._path, 'bauchan.temp.sh'))

    @property
    def agent_pid(self) -> int:
        return int(self._get('AgentPID', -1))

    @agent_pid.setter
    def agent_pid(self, value: int):
        self._set('AgentPID', value)

    @agent_pid.deleter
    def agent_pid(self):
        self._unset('AgentPID')


__all__ = [
    'configure_logging',
    'write_script',
    'Data',
]
