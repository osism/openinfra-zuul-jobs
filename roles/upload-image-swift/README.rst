Upload a filesystem image to a swift container

This uploads a filesystem image (for example, one built by diskimage
builder) to an OpenStack Object Store (Swift) container.  The role
returns an artifact to Zuul suitable for use by the zuul-launcher.

If a `raw` or `vhd` image is provided,
`upload_image_swift_compress_image` is true and the `zstd` command is
available, it will be compressed in the way that zuul-launcher
expects.

**Role Variables**

.. zuul:rolevar:: upload_image_swift_cloud_config

   Complex argument which contains the cloud configuration in
   os-cloud-config (clouds.yaml) format.  It is expected that this
   argument comes from a `Secret`.

.. zuul:rolevar:: upload_image_swift_container

   This role will create containers which do not already exist.

   Note that you will want to set this to a value that uniquely
   identifies your Zuul installation if using shared object stores that
   require globally unique container names. For example if using a
   public cloud whose Swift API is provided by Ceph.

   The container should be dedicated to image uploads so that the
   "delete_after" option may be safely used.

.. zuul:rolevar:: upload_image_swift_delete_after
   :default: 0

   Number of seconds to delete objects after upload. Default is 0
   (disabled).  This will tell swift to delete the file automatically,
   but if that fails, the next run of the role will attempt to delete
   any objects in the bucket older than this time.

.. zuul:rolevar:: upload_image_swift_image_name
   :default: `{{ build_diskimage_image_name | default(zuul.image_build_name) }}`

   The Zuul image name for use by zuul-launcher (e.g., `debian-bookworm`).

.. zuul:rolevar:: upload_image_swift_format

   The image format (e.g., `qcow2`).

.. zuul:rolevar:: upload_image_swift_extension
   :default: `{{ upload_image_swift_format }}`

   The extension to use when uploading (only used in the default
   values for the following variables.

.. zuul:rolevar:: upload_image_swift_filename
   :default: `{{ build_diskimage_image_root }}/{{ build_diskimage_image_name }}.{{ upload_image_swift_extension }}`

   The path of the local file to upload.

.. zuul:rolevar:: upload_image_swift_name
   :default: `{{ zuul.build }}-{{ build_diskimage_image_name }}.{{ upload_image_swift_extension }}`

   The object name to use when uploading.

.. zuul:rolevar:: upload_image_swift_compress_image
   :default: true

   Whether to compress the image using zstd before upload.

   Some providers may require the image to be in raw format when
   importing directly from object storage. In those cases the flag
   should be set to `false`.

.. zuul:rolevar:: upload_image_swift_hash_timeout
    :default: 86400

    The async timeout for md5/sha256 image hash tasks.
