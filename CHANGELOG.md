# 0.2.3 (Mar 2, 2021) -- Cleanup

## 🏠 Internal

- Mainly updating the release on PyPi to remove accidentally included
  remains of the previous osfclient fork.


# 0.2.2 (Feb 10, 2021) -- No forks

## 🏠 Internal

- The internal fork of osfclient has been removed and a dependency to
  version 0.0.5 (which comes with all necessary features) was added.


# 0.2.1 (Feb 1, 2021) -- Bugfix

## 🐛 Bug Fixes

- A bug that allowed to clone an OSF project from misshaped URLs of type
  osf://<project id>/some/where/underneath (was treated as osf://<project id>).
  This led to an infinite recursion when installing subdatasets.

## 🏠 Internal

- An internal function allows to update existing project metadata

- Updated internal osfclient fork

## 📝 Documentation

- Several tweaks to the documentation

## 🛡 Tests

- Changes in continuous integration testing with no implications for users


# 0.2.0 (Jul 17, 2020) -- More DataLad and OSF integration

## 💫 Enhancements and new features

This release brings a variety improvements that jointly better utilize
DataLad and OSF features

- Add the ability to query a credential store via DataLad, when no
  credentials are found in environment variables

- Add `osf-credentials` command to more conveniently set and reset
  OSF credentials for use by DataLad

- `create-sibling-osf` can now create public projects

- OSF projects are now of category `data` by default and another category
  can be set via `create-sibling-osf --category`

- Assign default OSF project tags to location any and specific datasets
  via OSF search functionality

- Add the ability to use OSF projects as git-annex exports or actual annex
  stores

- Add `git-remote-osf` Git remote helper to use an OSF project as a regular
  Git remote, using `osf://<projectid>` URLs. Performance can be suboptimal
  when used with `datalad push` in DataLad versions up to 0.13.0 (repeated,
  avoidable Git repository uploads). Fixes have been queue for 0.13.1, and
  0.14.0.

- Ability to `datalad clone osf://<projectid>` to publish and obtain entire
  datasets via OSF , without the use of a separate service for Git hosting

## 🪓 Deprecations, removals, API changes

- Rename `create-sibling-osf --sibling` to `-s/--name` for uniformity with
  other such DataLad commands

- Rename `create-sibling-osf --mode {annexstore,exporttree}` to
  `--mode {annex,export}` to match git-annex terminology

## 🛡 Tests

- Credential-less read-only access to public datasets

## 🐛 Bug Fixes

- User/password authentication used user as password and failed

## 🏠 Internal

- Dropped dependency on `7z`, archive and compression is now implemented via
  Python standard library functionality

- Major documentation overhaul to reflect the new features and changed behavior


# 0.1 (Jun 18, 2020) -- Sprint!

First implementation of a DataLad extension for exchanging data with and
via the Open Science Framework (OSF), completed during the OHBM brainhack
2020.

- A new git-annex special remote implementation `git-annex-remote-osf`
  is included that supports using an OSF project as a classic annex,
  but also supports `exporttree=yes`

- A `datalad create-sibling-osf` command is provided that can
  programmatically create OSF projects for dataset publication.
