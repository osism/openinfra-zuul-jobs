Ensure a pip-installed command is available

This role checks for the specified command, and if not found, installs
it via ``pip`` into a virtual environment for the current user.

The minimal required input is the command name. Additionally, you can
specify a version or a path to a local venv, among other things.

Example:

.. code-block:: yaml

   - role: ensure-python-command
     vars:
       ensure_python_command_name: poetry
       ensure_python_command_version: ==1.8.5  # omit to install latest

In this case, if the ``poetry`` command is not already available, pip
will install it in a new venv. Either way, after running this role, the
``ensure_python_command_executable`` variable will hold the full path to
the command.

**Role Variables**

.. zuul:rolevar:: ensure_python_command_name

   Required. The name of the command to ensure is available.

.. zuul:rolevar:: ensure_python_command_package
   :default: {{ ensure_python_command_name }}

   The name of the Python package that provides the desired command.
   Defaults to the command name, since this is usually the case.
   Set this variable when they differ.

.. zuul:rolevar:: ensure_python_command_version
   :default: ''

   The version specifier to select the version of the package to install.
   If omitted, the latest version will be installed.

.. zuul:rolevar:: ensure_python_command_existing
   :default: ''

   Look for an existing command at this specific path. For example, if your base
   image pre-installs the command in an out-of-path environment, set this so the
   role does not attempt to install the command again.

.. zuul:rolevar:: ensure_python_command_venv_path
   :default: {{ ansible_user_dir }}/.local/{{ ensure_python_command_package }}

   Directory for the Python venv where the package should be installed.

.. zuul:rolevar:: ensure_python_command_global_symlink
   :default: False

   Install a symlink to the command executable into ``/usr/local/bin/``.

   This can be useful when scripts need to be run that expect to find the
   command in a more standard location and plumbing through the value
   of ``ensure_python_command_executable`` would be onerous.

   Setting this requires root access, so should only be done in
   circumstances where root access is available.

**Output Variables**

.. zuul:rolevar:: ensure_python_command_executable

   The full path to the command executable, whether it was detected or
   installed by the role.
