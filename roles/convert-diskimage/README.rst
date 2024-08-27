This role converts diskimages from one format to other using the qemu-img tool.

Currently, only Ubuntu and Debian distributions are supported.

**Role variables**

.. zuul:rolevar:: convert_diskimage_source_image

   The path to the source image file.

.. zuul:rolevar::  convert_diskimage_target_image

   The path of the desired target image file.

.. zuul:rolevar::  convert_diskimage_target_image_formats
   :type: list

   The desired formats of the target image.
   Supported values are "raw" and "qcow2".
