This role installs diskimage-builder and dependencies.

Currently, only Ubuntu and Debian distributions are supported.

.. note::

   The disk-image-create script will be located in
   `{{ dib_venv_dir }}/bin/disk-image-create`.

**Role variables**

.. zuul:rolevar:: ensure_dib_venv_dir
   :default: "{{ ansible_user_dir }}/dib"

   Directory for the virtualenv to install the diskimage-builder.

.. zuul:rolevar:: ensure_dib_version
   :default: undefined

   The version of diskimage-builder to install. The default is to install the
   lastest version.

**Output Variables**

.. zuul:rolevar:: ensure_dib_command

   This variable points to the disk-image-create command installed in the
   {{ dib_venv_dir }}.
