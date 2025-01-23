Ensure twine is installed.

Look for ``twine``, and if not found, install it via ``pip`` into a
virtual environment for the current user.

**Role Variables**

.. zuul:rolevar:: ensure_twine_version
   :default: ''

   Version specifier to select the version of Twine.  The default is the
   latest version.

.. zuul:rolevar:: ensure_twine_venv_path
   :default: {{ ansible_user_dir }}/.local/twine

   Directory for the Python venv where Twine will be installed.

.. zuul:rolevar:: ensure_twine_global_symlink
   :default: False

   Install a symlink to the twine executable into ``/usr/local/bin/twine``.
   This can be useful when scripts need to be run that expect to find
   Twine in a more standard location and plumbing through the value
   of ``pypi_twine_executable`` would be onerous.

   Setting this requires root access, so should only be done in
   circumstances where root access is available.

**Output Variables**

.. zuul:rolevar:: pypi_twine_executable
   :default: twine

   After running this role, ``pypi_twine_executable`` will be set as the path
   to a valid ``twine``.

   At role runtime, look for an existing ``twine`` at this specific
   path.  Note the default (``twine``) effectively means to find twine in
   the current ``$PATH``.  For example, if your base image
   pre-installs twine in an out-of-path environment, set this so the
   role does not attempt to install the user version.
