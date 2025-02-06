Ensure uv is installed

Look for ``uv``, and if not found, install it via ``pip`` into a
virtual environment for the current user.

**Role Variables**

.. zuul:rolevar:: ensure_uv_version
   :default: ''

   Version specifier to select the version of uv.  The default is the
   latest version.

.. zuul:rolevar:: ensure_uv_venv_path
   :default: {{ ansible_user_dir }}/.local/uv

   Directory for the Python venv where uv will be installed.

.. zuul:rolevar:: ensure_uv_global_symlink
   :default: False

   Install a symlink to the uv executable into ``/usr/local/bin/uv``.
   This can be useful when scripts need to be run that expect to find
   uv in a more standard location and plumbing through the value
   of ``ensure_uv_executable`` would be onerous.

   Setting this requires root access, so should only be done in
   circumstances where root access is available.

**Output Variables**

.. zuul:rolevar:: ensure_uv_executable
   :default: uv

   After running this role, ``ensure_uv_executable`` will be set as the path
   to a valid ``uv``.

   At role runtime, look for an existing ``uv`` at this specific
   path.  Note the default (``uv``) effectively means to find uv in
   the current ``$PATH``.  For example, if your base image
   pre-installs uv in an out-of-path environment, set this so the
   role does not attempt to install the user version.
