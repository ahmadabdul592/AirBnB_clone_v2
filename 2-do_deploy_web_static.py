#!/usr/bin/python3
"""
    Distributes an archive to our web servers,
    using the function do_deploy
    def do_deploy(archive_path):
    Return False iff archive path doesn't exist
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['3.235.239.225', '35.170.64.18']
env.user = 'ubuntu'
env.identity = '~/.ssh/school'
env.password = None


def do_deploy(archive_path):
    """
    Deploys an archive to a server
    """
    if exists(archive_path) is False:
        return False
    try:
        file_N = archive_path.split("/")[-1]
        n = file_N.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}{}/'.format(path, n))
        run('sudo tar -xzf /tmp/{} -C {}{}/'.format(file_N, path, n))
        run('sudo rm /tmp/{}'.format(file_N))
        run('sudo mv {0}{1}/web_static/* {0}{1}/'.format(path, n))
        run('sudo rm -rf {}{}/web_static'.format(path, n))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {}{}/ /data/web_static/current'.format(path, n))
        run('sudo chmod -R 755 /data/')
        print("New version deployed!")
        return True
    except FileNotFoundError:
        return False
