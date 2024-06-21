Ensure specified python interpreter and development files are installed

There are three ways to install the python interpreter:

1. Using distribution packages: This is the default (``python_use_pyenv`` and
   ``python_use_stow`` are both ``false``).

2. Install using ``pyenv``.

3. Install using ``stow``.

.. note:: You cannot use both ``pyenv`` and ``stow`` method for the same job.
          That means that ``python_use_pyenv`` and ``python_use_stow``
          cannot be set both to ``True`` at the same time.

**Role Variables**

.. zuul:jobvar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   The project directory.  Serves as the location for version files for
   ``python_use_pyenv``.

.. zuul:rolevar:: python_version
   :type: str

   Optional version of python interpreter to install, such as ``3.7``.
   Note that you should use a string value for this variable rather than
   a float. This avoids problems with 3.10 being evaluated as 3.1.

.. zuul:rolevar:: python_use_pyenv
   :type: bool
   :default: False

   Whether to optionally use ``pyenv`` to install python instead of distro
   packages. If this is given without a ``python_version``,
   it will look for a ``.python-version`` file in the ``zuul_work_dir``.

.. zuul:rolevar:: python_use_stow
   :type: bool
   :default: False

   In case you have image with already prepared python versions, for example used the
   python-stow-versions element, you can activate them with stow utility
   by setting this variable to ``true``.

.. zuul:rolevar:: python_stow_dir
   :type: str
   :default: /usr/local/stow

   Sets the target directory for stow. This should be the path to the
   directory where prepared python packages are located.
