0.1 (Jun 18, 2020) -- Sprint!

- First implementation of a DataLad extension for exchanging data with and
  via the Open Science Framework (OSF), completed during the OHBM brainhack
  2020.

  - A new git-annex special remote implementation `git-annex-remote-osf`
    is included that supports using an OSF project as a classic annex,
    but also supports `exporttree=yes`

  - A `datalad create-sibling-osf` command is provided that can
    programmatically create OSF projects for dataset publication.
