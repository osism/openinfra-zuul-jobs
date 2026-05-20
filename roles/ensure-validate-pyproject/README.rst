Ensure validate-pyproject is installed.

Look for ``validate-pyproject``, and if not found, install it via ``pip`` into
a virtual environment for the current user.

**Role Variables**

.. zuul:rolevar:: ensure_validate_pyproject_version
   :default: ''

   Version specifier to select the version of validate-pyproject. The default
   is the latest version.

.. zuul:rolevar:: ensure_validate_pyproject_venv_path
   :default: {{ ansible_user_dir }}/.local/validate_pyproject

   Directory for the Python venv where validate-pyproject will be installed.

.. zuul:rolevar:: ensure_validate_pyproject_global_symlink
   :default: False

   Install a symlink to the validate-pyproject executable into
   ``/usr/local/bin/validate-pyproject``. This can be useful when scripts need
   to be run that expect to find validate-pyproject in a more standard location
   and plumbing through the value of ``validate_pyproject_executable`` would be
   onerous.

   Setting this requires root access, so should only be done in
   circumstances where root access is available.

**Output Variables**

.. zuul:rolevar:: validate_pyproject_executable
   :default: validate-pyproject

   After running this role, ``validate_pyproject_executable`` will be set
   as the path to a valid ``validate-pyproject``.

   At role runtime, look for an existing ``validate-pyproject`` at this
   specific path. Note the default (``validate-pyproject``) effectively means
   to find validate-pyproject in the current ``$PATH``. For example, if your
   base image pre-installs validate-pyproject in an out-of-path environment,
   set this so the role does not attempt to install the user version.
