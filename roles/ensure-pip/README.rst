Ensure pip is available

This role is intended install the requirements for the `pip module
<https://docs.ansible.com/ansible/latest/modules/pip_module.html>`__
on hosts.

Jobs that also wish to call ``pip`` via shell commands directly can
also use this to ensure ``pip`` is available.  However, it should be
noted that calling ``pip`` is ambiguous when supporting many
platforms.  On some platforms it may install the package under the
Python 2 interpreter and in others Python 3.  You should use a
qualified name (``pip2`` or ``pip3``) to avoid confusion.

This role will also install ``wheel`` components sufficient to run
``bdist_wheel`` builds or ``pip wheel`` on a source tree.

**Role Variables**

.. zuul:rolevar:: ensure_pip_from_packages
   :default: True

   Install the distribution packages for Python 3 pip, setuptools and
   wheel on the system.

.. zuul:rolevar:: ensure_pip_from_packages_with_python2
   :default: False

   Install the distribution packages for Python 2 pip, setuptools and
   wheel packages.  This defaults to ``True`` when Ansible is running
   under Python 2.

   CentOS 7 requies the ``epel`` repository if this flag is enabled
   because ``python-pip`` packages come from there.

   This may not be valid on distributions that have removed Python 2
   support.

.. zuul:rolevar:: ensure_pip_from_upstream
   :default: False

   Install pip from latest upstream sources locally.  Note this is
   probably not what you want and should be used with extreme caution.
   The installed pip does not coordinate with the system packaged
   versions, and can lead to wide variety of problems if CI jobs
   re-install ``pip`` packages, for example.

.. zuul:rolevar:: ensure_pip_from_upstream_interpreters
   :default: [ ansible_python_interpreter ]

   A list of interpreters to install pip from upstream with.  Note
   that by default the *last* entry in the list will likely own the
   ``/usr/local/bin/pip`` command; this can create confusion for
   legacy jobs if they assume ``pip`` installs Python 2 libraries but
   it is actually installing into the Python 3 environment.  This role
   does not install the Python 2 interpreter, which may not be
   available on the system, so caution should be used when specifying
   ``python2`` in this list.

.. zuul:rolevar:: ensure_pip_check_wheel
   :default: True

   In cases where a job needs to check for pip enough to make sure it can
   install pre-built wheel packages but shouldn't or can't install sdist
   tarballs by building them into wheels, setting this false will bypass the
   need to test for presence of the wheel module, which may not be available
   depending on the environment.

**Output Variables**

.. zuul:rolevar:: ensure_pip_virtualenv_command

   This variable will be set to a command appropriate for general
   usage with the ``pip`` module ``virtualenv_command`` argument on the
   host.  On Python 3 hosts this will be the inbuilt ``venv`` module, on
   Python 2 hosts the ``virtualenv`` package will be installed (this is
   avoided on Python 3 hosts as an unnecessary dependency).
