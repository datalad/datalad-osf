#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See LICENSE file distributed along with the datalad_osf package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##


import sys
from setuptools import setup
import versioneer

from _datalad_buildsupport.setup import (
    BuildManPage,
)

cmdclass = versioneer.get_cmdclass()
cmdclass.update(build_manpage=BuildManPage)

# Give setuptools a hint to complain if it's too old a version
# 30.3.0 allows us to put most metadata in setup.cfg
# Should match pyproject.toml
SETUP_REQUIRES = ['setuptools >= 30.3.0']
# This enables setuptools to install wheel on-the-fly
SETUP_REQUIRES += ['wheel'] if 'bdist_wheel' in sys.argv else []

if __name__ == '__main__':
    setup(name='datalad_osf',
          version=versioneer.get_version(),
          cmdclass=cmdclass,
          setup_requires=SETUP_REQUIRES,
          entry_points={
              # 'datalad.extensions' is THE entrypoint inspected by the datalad API builders
              'datalad.extensions': [
                  # the label in front of '=' is the command suite label
                  # the entrypoint can point to any symbol of any name, as long it is
                  # valid datalad interface specification (see demo in this extensions
                  'osf=datalad_osf:command_suite',
              ],
              'console_scripts': [
                  'git-remote-osf=datalad_osf.git_remote:main',
                  'git-annex-remote-osf=datalad_osf.annex_remote:main',
              ],
          },
    )

