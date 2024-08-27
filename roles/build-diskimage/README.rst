Role for building images using diskimage-builder.

Diskimage-builder and diskimage elements can be configured by passing
corresponding settings as environment variables to this role, or using
the ``build_diskimage_environment`` variable.

By default the `build-disk-image` command does not print its output to stdout,
but only to a log file in the configured log directory. To additionally log to
stdout, set `DIB_QUIET: 0` in `build_diskimage_environment`.

Example:

.. code-block:: yaml

   roles:
    - name: build-diskimage
      environment:
        ELEMENTS_PATH: /tmp/elements
        DIB_PYPI_MIRROR_URL: https://example.com

**Role variables**

.. zuul:rolevar:: build_diskimage_command
   :default: "{{ ensure_dib_command }}"

   Path to the build-disk-image command. This defaults to 
   {{ ensure_dib_command }}. as being set by the ensure-dib role.

.. zuul:rolevar:: build_diskimage_image_name

   Name of the image to build.

.. zuul:rolevar:: build_diskimage_formats
   :type: list
   :default: ['qcow2']

   List of image types to generate.

.. zuul:rolevar:: build_diskimage_elements
   :type: list
   :default: ['ubuntu', 'vm']

   List of elements that should be used when creating the disk image.

.. zuul:rolevar:: build_diskimage_environment
   :type: dict

   Environment variables for the diskimage builder command may be
   supplied using this variable (or by directly using the Ansible
   ``environment`` argument).

.. zuul:rolevar:: build_diskimage_image_root
   :default: "{{ ansible_user_dir }}/dib-images"

   Directory to store the build images.

.. zuul:rolevar:: build_diskimage_logs_dir
   :default: {{ ansible_user_dir }}/zuul-output/logs

   The path where the log output of the diskimage-builder shall be written to

.. zuul:rolevar:: build_diskimage_retry_limit
   :default: 0

   The number of times the build-diskimage command shall be retried until
   successful.

.. zuul:rolevar:: build_diskimage_retry_delay
   :default: 120

   The number of seconds to wait between retries of the build-diskimage
   command.
