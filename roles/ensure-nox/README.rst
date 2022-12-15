Ensure nox is installed

Look for ``nox``, and if not found, install it via ``pip`` into a
virtual environment for the current user.

**Role Variables**

.. zuul:rolevar:: ensure_nox_version
   :default: ''

   Version specifier to select the version of nox.  The default is the
   latest version.

**Output Variables**

.. zuul:rolevar:: nox_executable
   :default: nox

   After running this role, ``nox_executable`` will be set as the path
   to a valid ``nox``.

   At role runtime, look for an existing ``nox`` at this specific
   path.  Note the default (``nox``) effectively means to find tox in
   the current ``$PATH``.  For example, if your base image
   pre-installs tox in an out-of-path environment, set this so the
   role does not attempt to install the user version.
