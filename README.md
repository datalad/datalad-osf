# DataLad-OSF: Opening up the Open Science Framework for DataLad 
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-11-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

[![GitHub release](https://img.shields.io/github/release/datalad/datalad-osf.svg)](https://GitHub.com/datalad/datalad-osf/releases/) [![PyPI version fury.io](https://badge.fury.io/py/datalad-osf.svg)](https://pypi.python.org/pypi/datalad-osf/) [![Build status](https://ci.appveyor.com/api/projects/status/298n91oo1mla276t/branch/master?svg=true)](https://ci.appveyor.com/project/mih/datalad-osf/branch/master) [![codecov.io](https://codecov.io/github/datalad/datalad-osf/coverage.svg?branch=master)](https://codecov.io/github/datalad/datalad-osf?branch=master) [![docs](https://github.com/datalad/datalad-osf/workflows/docs/badge.svg)](https://github.com/datalad/datalad-osf/actions?query=workflow%3Adocs) [![Documentation Status](https://readthedocs.org/projects/datalad-osf/badge/?version=latest)](http://docs.datalad.org/projects/osf/en/latest/?badge=latest) [![DOI](https://zenodo.org/badge/272689400.svg)](https://zenodo.org/badge/latestdoi/272689400)


Welcome! This repository contains a [DataLad](http://datalad.org) extension that enables DataLad to work with the Open Science Framework (OSF). Use it to share, retrieve and collaborate on DataLad datasets via the OSF.

The development of this tool started at [OHBM Brainhack 2020](https://github.com/ohbm/hackathon2020/issues/156) in June 2020, coordinated in [this repository](https://github.com/adswa/git-annex-remote-osf). See our [documentation](http://docs.datalad.org/projects/osf) for more extensive information.

## Requirements

- Datalad: relies on [git-annex](http://docs.datalad.org/projects/osf/en/latest/git-annex.branchable.com/), [Git](http://docs.datalad.org/projects/osf/en/latest/git-scm.com/) and Python. If you don’t have DataLad installed yet, please follow the instructions [here](http://handbook.datalad.org/en/latest/intro/installation.html).
- Account on the [Open Science Framework (OSF)](https://osf.io/register)

## Installation

```
# create and enter a new virtual environment (optional)
$ virtualenv --python=python3 ~/env/dl-osf
$ . ~/env/dl-osf/bin/activate
# install from PyPi
$ pip install datalad-osf
```

## How to use

See our [documentation](http://docs.datalad.org/projects/osf/) for more info on how to use this tool and a tutorial on major use cases.

## How to contribute
You are very welcome to help out developing this tool further. You can contribute by:

- Creating an issue for bugs or tips for further development
- Making a pull request for any changes suggested by yourself
- Testing out the software and communicating your feedback to us

Please see our contributing guidelines for more information.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="http://psychoinformatics.de"><img src="https://avatars1.githubusercontent.com/u/136479?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Michael Hanke</b></sub></a><br /><a href="#maintenance-mih" title="Maintenance">🚧</a> <a href="https://github.com/datalad/datalad-osf/commits?author=mih" title="Code">💻</a> <a href="https://github.com/datalad/datalad-osf/issues?q=author%3Amih" title="Bug reports">🐛</a> <a href="#ideas-mih" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/DorienHuijser"><img src="https://avatars1.githubusercontent.com/u/58177697?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Dorien Huijser</b></sub></a><br /><a href="https://github.com/datalad/datalad-osf/commits?author=DorienHuijser" title="Documentation">📖</a> <a href="#projectManagement-DorienHuijser" title="Project Management">📆</a> <a href="#ideas-DorienHuijser" title="Ideas, Planning, & Feedback">🤔</a> <a href="#userTesting-DorienHuijser" title="User Testing">📓</a></td>
    <td align="center"><a href="https://github.com/TheDragon246"><img src="https://avatars2.githubusercontent.com/u/63247401?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ashish Sahoo</b></sub></a><br /><a href="https://github.com/datalad/datalad-osf/commits?author=TheDragon246" title="Documentation">📖</a> <a href="#maintenance-TheDragon246" title="Maintenance">🚧</a></td>
    <td align="center"><a href="https://github.com/SRSteinkamp"><img src="https://avatars2.githubusercontent.com/u/17494653?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Simon Steinkamp</b></sub></a><br /><a href="https://github.com/datalad/datalad-osf/commits?author=SRSteinkamp" title="Tests">⚠️</a> <a href="https://github.com/datalad/datalad-osf/commits?author=SRSteinkamp" title="Documentation">📖</a> <a href="#projectManagement-SRSteinkamp" title="Project Management">📆</a> <a href="#ideas-SRSteinkamp" title="Ideas, Planning, & Feedback">🤔</a> <a href="#userTesting-SRSteinkamp" title="User Testing">📓</a> <a href="#maintenance-SRSteinkamp" title="Maintenance">🚧</a></td>
    <td align="center"><a href="https://github.com/bpoldrack"><img src="https://avatars2.githubusercontent.com/u/10498301?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Benjamin Poldrack</b></sub></a><br /><a href="#projectManagement-bpoldrack" title="Project Management">📆</a> <a href="#ideas-bpoldrack" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/datalad/datalad-osf/commits?author=bpoldrack" title="Code">💻</a> <a href="#maintenance-bpoldrack" title="Maintenance">🚧</a></td>
    <td align="center"><a href="https://gitlab.com/kousu"><img src="https://avatars2.githubusercontent.com/u/987487?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Nick</b></sub></a><br /><a href="#projectManagement-kousu" title="Project Management">📆</a> <a href="#ideas-kousu" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/datalad/datalad-osf/commits?author=kousu" title="Code">💻</a> <a href="#maintenance-kousu" title="Maintenance">🚧</a></td>
    <td align="center"><a href="https://github.com/nbeliy"><img src="https://avatars0.githubusercontent.com/u/44231332?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Nikita Beliy</b></sub></a><br /><a href="#ideas-nbeliy" title="Ideas, Planning, & Feedback">🤔</a> <a href="#userTesting-nbeliy" title="User Testing">📓</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/mjboos"><img src="https://avatars0.githubusercontent.com/u/7125006?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Moritz J. Boos</b></sub></a><br /><a href="https://github.com/datalad/datalad-osf/commits?author=mjboos" title="Code">💻</a> <a href="#userTesting-mjboos" title="User Testing">📓</a> <a href="#ideas-mjboos" title="Ideas, Planning, & Feedback">🤔</a> <a href="#maintenance-mjboos" title="Maintenance">🚧</a></td>
    <td align="center"><a href="http://www.adina-wagner.com"><img src="https://avatars1.githubusercontent.com/u/29738718?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Adina Wagner</b></sub></a><br /><a href="#projectManagement-adswa" title="Project Management">📆</a> <a href="#ideas-adswa" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/datalad/datalad-osf/commits?author=adswa" title="Code">💻</a> <a href="https://github.com/datalad/datalad-osf/commits?author=adswa" title="Documentation">📖</a> <a href="#maintenance-adswa" title="Maintenance">🚧</a></td>
    <td align="center"><a href="https://www.stefanappelhoff.com"><img src="https://avatars1.githubusercontent.com/u/9084751?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Stefan Appelhoff</b></sub></a><br /><a href="https://github.com/datalad/datalad-osf/commits?author=sappelhoff" title="Documentation">📖</a> <a href="#userTesting-sappelhoff" title="User Testing">📓</a></td>
    <td align="center"><a href="https://github.com/thomasrockhu-codecov"><img src="https://avatars.githubusercontent.com/u/88201630?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Tom Hu</b></sub></a><br /><a href="#infra-thomasrockhu-codecov" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Acknowledgements

This DataLad extension was developed with support from the German Federal
Ministry of Education and Research (BMBF 01GQ1905), and the US National Science
Foundation (NSF 1912266).
