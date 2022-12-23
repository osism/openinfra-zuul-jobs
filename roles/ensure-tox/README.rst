Ensure tox is installed

Look for ``tox``, and if not found, install it via ``pip`` into a
virtual environment for the current user.

**Role Variables**

.. zuul:rolevar:: ensure_tox_version
   :default: ''

   Version specifier to select the version of tox. For example if your
   project is not compatible with tox v4 you can set this value to
   `<4` to install the latest v3 release. The default is '' which
   installs latest.

.. zuul:rolevar:: tox_prefer_python2
   :default: False

   If tox is not detected, prefer to install tox inside Python 2
   instead of Python 3.

   If set,
   :zuul:rolevar:`ensure-pip.ensure_pip_from_packages_with_python2`
   will be automatically set to `True` to enable a Python 2
   installation of `pip`.

.. zuul:rolevar:: ensure_global_symlinks
   :default: False

   Install a symlink to the tox executable into ``/usr/local/bin/tox``.
   This can be useful when scripts need to be run that expect to find
   tox in a more standard location and plumbing through the value
   of ``tox_executable`` would be onerous.

   Setting this requires root access, so should only be done in
   circumstances where root access is available.

**Output Variables**

.. zuul:rolevar:: tox_executable
   :default: tox

   After running this role, ``tox_executable`` will be set as the path
   to a valid ``tox``.

   At role runtime, look for an existing ``tox`` at this specific
   path.  Note the default (``tox``) effectively means to find tox in
   the current ``$PATH``.  For example, if your base image
   pre-installs tox in an out-of-path environment, set this so the
   role does not attempt to install the user version.
