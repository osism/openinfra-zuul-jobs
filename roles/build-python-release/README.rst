Build sdist and wheel for Python projects.

**Role Variables**

.. zuul:rolevar:: build_wheel
   :default: true

   Whether to build a wheel. Set to false to just build an sdist tarball.

.. zuul:rolevar:: legacy_setup
   :default: false

   By default, the role uses pyproject-build. Set this to true if you need
   to use old-style direct invocation of setup.py instead.

.. zuul:rolevar:: release_python
   :default: python

   The python interpreter to use. Set it to "python3" to use python 3,
   for example. Only relevant when legacy_setup is enabled.

.. zuul:rolevar:: bdist_wheel_xargs
   :default: ''

   Extra arguments to pass to the bdist_wheel command when building
   packages. Only relevant when legacy_setup is enabled.
