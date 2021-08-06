# Author: Michel Lopez <Lo0p1nG 404>

import platform

from setuptools import find_packages, setup

setup(name="attack_info",
      version="0.0.1",

      author="Michel Lopez",
      author_email="looping404@protonmail.com",

      maintainer="Lo0p1nG 404",
      maintainer_email="looping404@protonmail.com",

      description="Gatering attack enumeration information in a markdown note",
      long_description="README.md",

      url="https://github",

      packages=find_packages(),

      package_data={
          '': [],
      },

      platforms=[platform.platform()],

      install_requires=[
          'pystache', 'tomark'
      ],

      keywords="enumeration, markdown, summary, s4vitar",

      classifiers=["Development Status :: 1 - Beta",
                   "Environment :: Console",
                   "Intended Audience :: Science/Research",
                   "Intended Audience :: Developers",
                   "License :: CC BY-NC-SA 4.0",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3",
                   "Topic :: Software Development :: Code Generators",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   "Topic :: Utilities"]
      )
