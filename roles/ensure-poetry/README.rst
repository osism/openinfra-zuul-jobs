Ensure Poetry is installed

Look for ``poetry``, and if not found, install it via ``pip`` into a
virtual environment for the current user.

**Role Variables**

.. zuul:rolevar:: ensure_poetry_version
   :default: ''

   Version specifier to select the version of Poetry.  The default is the
   latest version.

.. zuul:rolevar:: ensure_poetry_venv_path
   :default: {{ ansible_user_dir }}/.local/poetry

   Directory for the Python venv where Poetry will be installed.

.. zuul:rolevar:: ensure_poetry_global_symlink
   :default: False

   Install a symlink to the poetry executable into ``/usr/local/bin/poetry``.
   This can be useful when scripts need to be run that expect to find
   Poetry in a more standard location and plumbing through the value
   of ``ensure_poetry_executable`` would be onerous.

   Setting this requires root access, so should only be done in
   circumstances where root access is available.

**Output Variables**

.. zuul:rolevar:: ensure_poetry_executable
   :default: poetry

   After running this role, ``ensure_poetry_executable`` will be set as the path
   to a valid ``poetry``.

   At role runtime, look for an existing ``poetry`` at this specific
   path.  Note the default (``poetry``) effectively means to find poetry in
   the current ``$PATH``.  For example, if your base image
   pre-installs poetry in an out-of-path environment, set this so the
   role does not attempt to install the user version.
