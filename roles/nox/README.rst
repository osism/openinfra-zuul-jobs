Runs nox for a project

This role overrides Python packages installed into nox environments with
corresponding Zuul sibling projects and runs nox tests as follows:

#. Create nox environments. Note this role currently relies on using
   the default .nox/session name environment paths.
#. Get Python sibling package names for sibling projects created by
   Zuul (using ``required-projects`` job variable). Package names are
   searched in following sources:

   * ``setup.cfg`` of *pbr* projects,
   * ``setup.py``,
   * ``nox_package_name`` role variable.

#. Remove sibling packages from nox environments.
#. Create temporary constraints file, lines for sibling packages are
   removed.
#. Install sibling packages from Zuul projects into nox environments
   with temporary constraints file.
#. Run nox tests.

**Role Variables**

.. zuul:rolevar:: nox_environment
   :type: dict
   :default: { "CI": "1" }

   Environment variables to pass in to the nox run. Nox behaves differently
   when the CI env var is set. We set that by default but allow you to
   override it if the CI behaviors are not desireable.

.. zuul:rolevar:: nox_session

   Space separated string listing nox sessions to run.

.. zuul:rolevar:: nox_keyword

   String to select nox sessions via keyword rather than session name.

.. zuul:rolevar:: nox_tag

   String to select nox sessions via tag rather than session name.

.. zuul:rolevar:: nox_force_python

   String to force a specific python version to be used in the session.
   This allows you to request session `tests` be run against python `3.11`.

.. zuul:rolevar:: nox_executable
   :default: nox

   Location of the nox executable.

.. zuul:rolevar:: nox_config_file

   Path to a nox configuration file. If not specified the nox will look
   for noxfile.py by default.

.. zuul:rolevar:: nox_extra_args
   :default: -v

   String of extra command line options to pass to nox.

.. zuul:rolevar:: nox_constraints_file

   Path to a pip constraints file. Will be provided to nox via
   ``NOX_CONSTRAINTS_FILE``.

.. zuul:rolevar:: nox_inline_comments
   :default: true

   Flag controlling whether to parse the output from the nox session
   and return inline comments to Zuul. Defaults to True.

.. zuul:rolevar:: nox_install_siblings
   :default: true

   Flag controlling whether to attempt to install python packages from any
   other source code repos zuul has checked out. Defaults to True.

.. zuul:rolevar:: nox_package_name

   Allows a user to setup the package name to be used by nox, over reading
   a setup.cfg file in the project.

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to run nox in.
