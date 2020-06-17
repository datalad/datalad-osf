DataLad extension to interface with OSF
***************************************

This extension allow DataLad to use the Open Science 
Framework (OSF_) as a SpecialRemote using ``git-annex`` and the ``osfclient``. 
So that code and DataLad datasets can live on a Remote, for example Github,
while the data is stored on OSF.
The extension was created during the OHBM Hackathon 2020.


.. toctree::

   acknowledgments

Documentation
=============

.. toctree:: 
   :maxdepth: 2

   intro
   settingup
   running
   example
   contact


API
===

High-level API commands
-----------------------

.. currentmodule:: datalad.api
.. autosummary::
   :toctree: generated

   osf_cmd


Command line reference
----------------------

.. toctree::
   :maxdepth: 1

   generated/man/datalad-osf-cmd



Git-annex utilities
-------------------

.. currentmodule:: datalad_osf
.. autosummary::
   :toctree: generated

   remote.OSFRemote


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |---| unicode:: U+02014 .. em dash

.. _OSF: http://www.osf.io/
