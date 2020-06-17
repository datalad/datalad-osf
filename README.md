# DataLad extension for working with the Open Science Framework
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

[![Travis tests status](https://secure.travis-ci.org/datalad/datalad-osf.png?branch=master)](https://travis-ci.org/datalad/datalad-osf) [![codecov.io](https://codecov.io/github/datalad/datalad-osf/coverage.svg?branch=master)](https://codecov.io/github/datalad/datalad-osf?branch=master) [![crippled-filesystems](https://github.com/datalad/datalad-osf/workflows/crippled-filesystems/badge.svg)](https://github.com/datalad/datalad-osf/actions?query=workflow%3Acrippled-filesystems) [![win2019](https://github.com/datalad/datalad-osf/workflows/win2019/badge.svg)](https://github.com/datalad/datalad-osf/actions?query=workflow%3Awin2019)  [![docs](https://github.com/datalad/datalad-osf/workflows/docs/badge.svg)](https://github.com/datalad/datalad-osf/actions?query=workflow%3Adocs)

Welcome! This repository contains a [DataLad](http://datalad.org) extension that equips DataLad with tools to interoperate with projects on the [Open Science Framework (OSF)](https://osf.io). Specifically, we attempt to create a git-annex special remote implementation to transform OSF storage into git-annex repositories. Files in OSF storage could thus be consumed or exported fast and easily via git-annex or datalad, and published to repository-hosting services (GitHub, GitLab, Bitbucket, ...) as lightweight repositories that constitute an alternative access to the data stored on the OSF - that is: you can git clone a repository from for example GitHub and get the data from the OSF from the command line or in your scripts.

The development of this tool started at [OHBM Brainhack 2020](https://github.com/ohbm/hackathon2020/issues/156) in June 2020, coordinated in [this repository](https://github.com/adswa/git-annex-remote-osf). See our [documentation](http://docs.datalad.org/projects/osf) for more extensive information.

## Required software

- Datalad
- Git
- git-annex
- Python 3

## Install

```
pip install -r requirements.txt # TODO merge into setup.py
pip install [--user] .
```

## How to contribute
You are very welcome to help out developing this tool further. You can contribute by:

- Creating an issue for bugs or tips for further development
- Making a pull request for any changes suggested by yourself
- Testing out the software and communicating your feedback to us

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="http://psychoinformatics.de"><img src="https://avatars1.githubusercontent.com/u/136479?v=4" width="100px;" alt=""/><br /><sub><b>Michael Hanke</b></sub></a><br /><a href="#maintenance-mih" title="Maintenance">🚧</a> <a href="https://github.com/datalad/datalad-osf/commits?author=mih" title="Code">💻</a> <a href="https://github.com/datalad/datalad-osf/issues?q=author%3Amih" title="Bug reports">🐛</a> <a href="#ideas-mih" title="Ideas, Planning, & Feedback">🤔</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="http://www.adina-wagner.com"><img src="https://avatars1.githubusercontent.com/u/29738718?v=4" width="100px;" alt=""/><br /><sub><b>Adina Wagner</b></sub></a><br /><a href="#projectManagement-adswa" title="Project Management">📆</a> <a href="#maintenance-adswa" title="Maintenance">🚧</a> <a href="https://github.com/adswa/git-annex-remote-osf/commits?author=adswa" title="Code">💻</a> <a href="https://github.com/adswa/git-annex-remote-osf/commits?author=adswa" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/DorienHuijser"><img src="https://avatars1.githubusercontent.com/u/58177697?v=4" width="100px;" alt=""/><br /><sub><b>Dorien Huijser</b></sub></a><br /><a href="https://github.com/adswa/git-annex-remote-osf/commits?author=DorienHuijser" title="Documentation">📖</a> <a href="#projectManagement-DorienHuijser" title="Project Management">📆</a> <a href="#ideas-DorienHuijser" title="Ideas, Planning, & Feedback">🤔</a> <a href="#userTesting-DorienHuijser" title="User Testing">📓</a> <a href="#maintenance-DorienHuijser" title="Maintenance">🚧</a></td>
    <td align="center"><a href="https://github.com/TheDragon246"><img src="https://avatars2.githubusercontent.com/u/63247401?v=4" width="100px;" alt=""/><br /><sub><b>Ashish Sahoo</b></sub></a><br /><a href="https://github.com/adswa/git-annex-remote-osf/commits?author=TheDragon246" title="Documentation">📖</a> <a href="#maintenance-TheDragon246" title="Maintenance">🚧</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
