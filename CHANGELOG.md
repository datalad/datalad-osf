0.2.0 (Jul 17, 2020) -- More DataLad and OSF integration

- This release brings a variety improvements that jointly better utilize
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

- API changes

  - Rename `create-sibling-osf --sibling` to `-s/--name` for uniformity with
    other such DataLad commands

  - Rename `create-sibling-osf --mode {annexstore,exporttree}` to
    `--mode {annex,export}` to match git-annex terminology

- Expanded test suite

  - Credential-less read-only access to public datasets

- Fixes

  - User/password authentication used user as password and failed

- Dropped dependency on `7z`, archive and compression is now implemented via
  Python standard library functionality

- Major documentation overhaul to reflect the new features and changed behavior


0.1 (Jun 18, 2020) -- Sprint!

- First implementation of a DataLad extension for exchanging data with and
  via the Open Science Framework (OSF), completed during the OHBM brainhack
  2020.

  - A new git-annex special remote implementation `git-annex-remote-osf`
    is included that supports using an OSF project as a classic annex,
    but also supports `exporttree=yes`

  - A `datalad create-sibling-osf` command is provided that can
    programmatically create OSF projects for dataset publication.
