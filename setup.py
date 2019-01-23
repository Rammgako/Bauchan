import os

from setuptools import setup, Command
import subprocess
import sys


class BuildWebExtensionCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.run(
            args=['npm', 'run', 'build'],
            cwd=os.path.join('.', 'extension'),
            stdout=sys.stdout,
            stderr=sys.stderr,
        )


setup(
    name='Bauchan',
    app=['bauchand.py'],
    data_files=[],
    options=dict(
        py2app=dict(
            plist=dict(
                Label='org.example.bauchan',
                LSUIElement=True,
                RunAtLoad=True,
                LaunchOnlyOnce=True,
                ProgramArguments=['Contents/MacOS/Bauchan'],
                Disabled=False,
                ProcessType='Interactive',
            ),
            resources=[
                'bauchan.py',
                'common.py',
                'org.example.bauchan.agent.plist',
            ]
        )
    ),
    setup_requires=[
        'py2app',
    ],
    install_requires=[
        'rumps',
    ],
    cmdclass={
        'build_webextension': BuildWebExtensionCommand,
    }
)
