Promote one or more previously uploaded container images.

.. include:: ../../roles/build-container-image/common.rst

.. zuul:rolevar:: promote_container_image_method
   :type: string
   :default: tag

   If ``tag`` (the default), then this role will update tags created
   by the upload-container-image role.  Set to
   ``intermediate-registry`` to have this role copy an image created
   and pushed to an intermediate registry by the build-container-role.
