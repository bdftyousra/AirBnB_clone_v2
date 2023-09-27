#!/usr/bin/python3
"""generates a .tgz archive from the contents of the web_static folder
"""
from datetime import datetime
from fabric.api import local


def do_pack():
    """generate
    """
    try:
        local("mkdir -p versions")
        res = local("tar -cvzf versions/web_static_{}.tgz web_static"
                    .format(datetime.now().strftime("%Y%m%d%H%M%S")),
                    capture=True)
        return res
    except Exception:
        return None
