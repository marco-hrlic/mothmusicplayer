
#!/usr/bin/env python2

from setuptools import setup

setup(  name="mothmusicplayer3",
        version="0.01",
        description="music player",
        author="Marco Hrlic",
        author_email="marco.hrlic@gmail.com",
        packages=["mothmusicplayer3"],
        scripts=["bin/mothmusicplayer3"],
        install_requires = ["mutagenx", "python3-keybinder"],
        include_package_data=True)


