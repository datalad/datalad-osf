# Contributing to Datalad-OSF

These contributing guidelines have been adjusted from: https://github.com/datalad/datalad/blob/master/CONTRIBUTING.md

## General
You are very welcome to help out developing this tool further. You can contribute by:

- Creating an issue for bugs or tips for further development
- Making a pull request for any changes suggested by yourself
- Testing out the software and communicating your feedback to us

**Note**: we have a public OSF repository on which you can test the software yourself if you do not have an OSF account: https://osf.io/zhcqw/

## How to contribute
The preferred way to contribute to this repository is
to fork the [master branch of this repository](https://github.com/datalad/datalad-osf/tree/master) on GitHub.  
Note that you can test the software on our [Testing repository on Open Science Framework](https://osf.io/zhcqw/).

Here we outline the workflow used by the developers:

0. Have a clone of our main [project repository][gh-datalad] as `origin`
   remote in your git:

          git clone git://github.com/datalad/datalad-osf

1. Fork the [master branch of this repository](https://github.com/datalad/datalad-osf/tree/master): click on the 'Fork'
   button near the top of the page.  This creates a copy of the code
   base under your account on the GitHub server.

2. Add your forked clone as a remote to the local clone you already have on your
   local disk:

          git remote add gh-YourLogin git@github.com:YourLogin/datalad-osf.git
          git fetch gh-YourLogin

    To ease addition of other github repositories as remotes, here is
    a little bash function/script to add to your `~/.bashrc`:

        ghremote () {
                url="$1"
                proj=${url##*/}
                url_=${url%/*}
                login=${url_##*/}
                git remote add gh-$login $url
                git fetch gh-$login
        }

    thus you could simply run:

         ghremote git@github.com:YourLogin/datalad-osf.git

    to add the above `gh-YourLogin` remote.  Additional handy aliases
    such as `ghpr` (to fetch existing pr from someone's remote) and 
    `ghsendpr` could be found at [yarikoptic's bash config file](http://git.onerussian.com/?p=etc/bash.git;a=blob;f=.bash/bashrc/30_aliases_sh;hb=HEAD#l865)

3. Create a branch (generally off the `origin/master`) to hold your changes:

          git checkout -b nf-my-feature

    and start making changes. Ideally, use a prefix signaling the purpose of the
    branch
    - `nf-` for new features
    - `bf-` for bug fixes
    - `rf-` for refactoring
    - `doc-` for documentation contributions (including in the code docstrings).
    - `bm-` for changes to benchmarks
    We recommend to **not** work in the ``master`` branch!

4. Work on this copy on your computer using Git to do the version control. When
   you're done editing, do:

          git add modified_files
          git commit

   to record your changes in Git.  Ideally, prefix your commit messages with the
   `NF`, `BF`, `RF`, `DOC`, `BM` similar to the branch name prefixes, but you could
   also use `TST` for commits concerned solely with tests, and `BK` to signal
   that the commit causes a breakage (e.g. of tests) at that point.  Multiple
   entries could be listed joined with a `+` (e.g. `rf+doc-`).  See `git log` for
   examples.  If a commit closes an existing DataLad issue, then add to the end
   of the message `(Closes #ISSUE_NUMER)`

5. Push to GitHub with:

          git push -u gh-YourLogin nf-my-feature

   Finally, go to the web page of your fork of the DataLad repo, and click
   'Pull request' (PR) to send your changes to the maintainers for review. This
   will send an email to the committers.  You can commit new changes to this branch
   and keep pushing to your remote -- github automagically adds them to your
   previously opened PR.

(If any of the above seems like magic to you, then look up the
[Git documentation](http://git-scm.com/documentation) on the web.)


Documentation
-------------
You can find our user documentation [here](http://docs.datalad.org/projects/osf).

### Docstrings

We use [NumPy standard] for the description of parameters docstrings.  If you are using
PyCharm, set your project settings (`Tools` -> `Python integrated tools` -> `Docstring format`).

[NumPy standard]: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt#docstring-standard

In addition, we follow the guidelines of [Restructured Text] with the additional features and treatments
provided by [Sphinx].

[Restructured Text]: http://docutils.sourceforge.net/docs/user/rst/quickstart.html
[Sphinx]: http://www.sphinx-doc.org/en/stable/

Additional Hints
----------------

### Merge commits

For merge commits to have more informative description, add to your
`.git/config` or `~/.gitconfig` following section:

    [merge]
    log = true

and if conflicts occur, provide short summary on how they were resolved
in "Conflicts" listing within the merge commit
(see [example](https://github.com/datalad/datalad/commit/eb062a8009d160ae51929998771964738636dcc2)).


Quality Assurance
-----------------

It is recommended to check that your contribution complies with the following
rules before submitting a pull request:

- All public methods should have informative docstrings with sample usage
  presented as doctests when appropriate.
- All other tests pass when everything is rebuilt from scratch.
- New code should be accompanied by tests.


Recognizing contributions
-------------------------

We welcome and recognize all contributions from documentation to testing to code development. 
You can see a list of current contributors in our [readme file](https://github.com/datalad/datalad-osf/blob/master/README.md).
For recognizing contributions, we use the **all-contributors bot**, which isinstalled in this repository. You can simply ask the bot
to add you as a contributor in every issue or pull request with this format:
`@all-contributors please add @gitusername for contribution1 contribution2`

Example: `@all-contributors please add @adswa for projectManagement maintenance code doc`
See the [emoji key](https://allcontributors.org/docs/en/emoji-key) for the different contributions.

Thank you!
----------

You're awesome. :wave::smiley:



Various hints for developers
----------------------------

### Useful tools

- While performing IO/net heavy operations use [dstat](http://dag.wieers.com/home-made/dstat)
  for quick logging of various health stats in a separate terminal window:
  
        dstat -c --top-cpu -d --top-bio --top-latency --net

- To monitor speed of any data pipelining [pv](http://www.ivarch.com/programs/pv.shtml) is really handy,
  just plug it in the middle of your pipe.

- For remote debugging epdb could be used (avail in pip) by using
  `import epdb; epdb.serve()` in Python code and then connecting to it with
  `python -c "import epdb; epdb.connect()".`

- We are using codecov which has extensions for the popular browsers
  (Firefox, Chrome) which annotates pull requests on github regarding changed coverage.

### Useful Environment Variables
Refer datalad/config.py for information on how to add these environment variables to the config file and their naming convention

- *DATALAD_DATASETS_TOPURL*:
  Used to point to an alternative location for `///` dataset. If running
  tests preferred to be set to http://datasets-tests.datalad.org
- *DATALAD_LOG_LEVEL*:
  Used for control the verbosity of logs printed to stdout while running datalad commands/debugging
- *DATALAD_LOG_CMD_OUTPUTS*:
  Used to control either both stdout and stderr of external commands execution are logged in detail (at DEBUG level)
- *DATALAD_LOG_CMD_ENV*:
  If contains a digit (e.g. 1), would log entire environment passed into
  the Runner.run's popen call.  Otherwise could be a comma separated list
  of environment variables to log
- *DATALAD_LOG_CMD_STDIN*:
  Whether to log stdin for the command
- *DATALAD_LOG_CMD_CWD*:
  Whether to log cwd where command to be executed
- *DATALAD_LOG_PID*
  To instruct datalad to log PID of the process
- *DATALAD_LOG_TARGET*
  Where to log: `stderr` (default), `stdout`, or another filename
- *DATALAD_LOG_TIMESTAMP*:
  Used to add timestamp to datalad logs
- *DATALAD_LOG_TRACEBACK*:
  Runs TraceBack function with collide set to True, if this flag is set to 'collide'.
  This replaces any common prefix between current traceback log and previous invocation with "..."
- *DATALAD_LOG_VMEM*:
  Reports memory utilization (resident/virtual) at every log line, needs `psutil` module
- *DATALAD_EXC_STR_TBLIMIT*: 
  This flag is used by the datalad extract_tb function which extracts and formats stack-traces.
  It caps the number of lines to DATALAD_EXC_STR_TBLIMIT of pre-processed entries from traceback.
- *DATALAD_SEED*:
  To seed Python's `random` RNG, which will also be used for generation of dataset UUIDs to make
  those random values reproducible.  You might want also to set all the relevant git config variables
  like we do in one of the travis runs
- *DATALAD_TESTS_TEMP_KEEP*: 
  Function rmtemp will not remove temporary file/directory created for testing if this flag is set
- *DATALAD_TESTS_TEMP_DIR*: 
  Create a temporary directory at location specified by this flag.
  It is used by tests to create a temporary git directory while testing git annex archives etc
- *DATALAD_TESTS_NONETWORK*: 
  Skips network tests completely if this flag is set
  Examples include test for s3, git_repositories, openfmri etc
- *DATALAD_TESTS_SSH*: 
  Skips SSH tests if this flag is **not** set
- *DATALAD_TESTS_NOTEARDOWN*: 
  Does not execute teardown_package which cleans up temp files and directories created by tests if this flag is set
- *DATALAD_TESTS_USECASSETTE*:
  Specifies the location of the file to record network transactions by the VCR module.
  Currently used by when testing custom special remotes
- *DATALAD_TESTS_OBSCURE_PREFIX*:
  A string to prefix the most obscure (but supported by the filesystem test filename
- *DATALAD_TESTS_PROTOCOLREMOTE*:
  Binary flag to specify whether to test protocol interactions of custom remote with annex
- *DATALAD_TESTS_RUNCMDLINE*:
  Binary flag to specify if shell testing using shunit2 to be carried out
- *DATALAD_TESTS_TEMP_FS*:
  Specify the temporary file system to use as loop device for testing DATALAD_TESTS_TEMP_DIR creation
- *DATALAD_TESTS_TEMP_FSSIZE*:
  Specify the size of temporary file system to use as loop device for testing DATALAD_TESTS_TEMP_DIR creation
- *DATALAD_TESTS_NONLO*:
  Specifies network interfaces to bring down/up for testing. Currently used by travis.
- *DATALAD_CMD_PROTOCOL*: 
  Specifies the protocol number used by the Runner to note shell command or python function call times and allows for dry runs. 
  'externals-time' for ExecutionTimeExternalsProtocol, 'time' for ExecutionTimeProtocol and 'null' for NullProtocol.
  Any new DATALAD_CMD_PROTOCOL has to implement datalad.support.protocol.ProtocolInterface
- *DATALAD_CMD_PROTOCOL_PREFIX*: 
  Sets a prefix to add before the command call times are noted by DATALAD_CMD_PROTOCOL.
- *DATALAD_USE_DEFAULT_GIT*:
  Instructs to use `git` as available in current environment, and not the one which possibly comes with git-annex (default behavior).
- *DATALAD_ASSERT_NO_OPEN_FILES*:
  Instructs test helpers to check for open files at the end of a test. If set, remaining open files are logged at ERROR level. Alternative modes are: "assert" (raise AssertionError if any open file is found), "pdb"/"epdb" (drop into debugger when open files are found, info on files is provided in a "files" dictionary, mapping filenames to psutil process objects).
- *DATALAD_ALLOW_FAIL*:
  Instructs `@never_fail` decorator to allow to fail, e.g. to ease debugging.

