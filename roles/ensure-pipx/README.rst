Ensure pipx is installed

Look for ``pipx``, and if not found, install it via ``pip`` into a
virtual environment for the current user.

**Role Variables**

.. zuul:rolevar:: ensure_pipx_version
   :default: ''

   Version specifier to select the version of pipx.  The default is the
   latest version.

.. zuul:rolevar:: ensure_pipx_venv_path
   :default: {{ ansible_user_dir }}/.local/pipx

   Directory for the Python venv where pipx will be installed.

.. zuul:rolevar:: ensure_pipx_global_symlink
   :default: False

   Install a symlink to the pipx executable into ``/usr/local/bin/pipx``.
   This can be useful when scripts need to be run that expect to find
   pipx in a more standard location and plumbing through the value
   of ``ensure_pipx_executable`` would be onerous.

   Setting this requires root access, so should only be done in
   circumstances where root access is available.

**Output Variables**

.. zuul:rolevar:: ensure_pipx_executable
   :default: pipx

   After running this role, ``ensure_pipx_executable`` will be set as the path
   to a valid ``pipx``.

   At role runtime, look for an existing ``pipx`` at this specific
   path.  Note the default (``pipx``) effectively means to find pipx in
   the current ``$PATH``.  For example, if your base image
   pre-installs pipx in an out-of-path environment, set this so the
   role does not attempt to install the user version.
