Ensure pyproject-build is installed

Look for ``pyproject-build``, and if not found, install it via ``pip`` into a
virtual environment for the current user.

**Role Variables**

.. zuul:rolevar:: ensure_pyproject_build_version
   :default: ''

   Version specifier to select the version of pyproject-build.  The default is
   the latest version.

.. zuul:rolevar:: ensure_pyproject_build_venv_path
   :default: {{ ansible_user_dir }}/.local/pyproject-build

   Directory for the Python venv where pyproject-build will be installed.

.. zuul:rolevar:: ensure_pyproject_build_global_symlink
   :default: False

   Install a symlink to the pyproject-build executable into
   ``/usr/local/bin/pyproject-build``. This can be useful when scripts need to
   be run that expect to find pyproject-build in a more standard location and
   plumbing through the value of ``ensure_pyproject_build_executable`` would be
   onerous.

   Setting this requires root access, so should only be done in
   circumstances where root access is available.

**Output Variables**

.. zuul:rolevar:: ensure_pyproject_build_executable
   :default: pyproject-build

   After running this role, ``ensure_pyproject_build_executable`` will be set
   as the path to a valid ``pyproject-build``.

   At role runtime, look for an existing ``pyproject-build`` at this specific
   path.  Note the default (``pyproject-build``) effectively means to find
   pyproject-build in the current ``$PATH``.  For example, if your base image
   pre-installs pyproject-build in an out-of-path environment, set this so the
   role does not attempt to install the user version.
