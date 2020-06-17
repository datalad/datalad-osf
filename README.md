# DataLad extension for working with the Open Science Framework
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
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
pip install [--user] .
```

## How to contribute
You are very welcome to help out developing this tool further. You can contribute by:

- Creating an issue for bugs or tips for further development
- Making a pull request for any changes suggested by yourself
- Testing out the software and communicating your feedback to us

## Contributors ✨
