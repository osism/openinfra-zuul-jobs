Upload a filesystem image to an S3 bucket

This uploads a filesystem image (for example, one built by diskimage
builder) to an S3 bucket.  The role returns an artifact to Zuul
suitable for use by the zuul-launcher.

**Role Variables**

.. zuul:rolevar:: upload_image_s3_endpoint

   The endpoint to use when uploading an image to an s3 compatible
   service.  By default this will be automatically constructed by boto
   but should be set when working with non-AWS hosted s3 service.

.. zuul:rolevar:: upload_image_s3_aws_access_key

   AWS access key to use.

.. zuul:rolevar:: upload_image_s3_aws_secret_key

   AWS secret key for the AWS access key.

.. zuul:rolevar:: upload_image_s3_bucket

   This role *will not* create buckets which do not already exist.

   Note that you will want to set this to a value that uniquely
   identifies your Zuul installation.

   The bucket should be dedicated to image uploads so that the
   "delete_after" option may be safely used.

.. zuul:rolevar:: upload_image_s3_delete_after
   :default: 0

   Number of seconds to delete objects after upload. Default is 0
   (disabled).  Each run of the role will attempt to delete any
   objects in the bucket older than this time.

   It is also recommended to use the AWS console to configure
   automatic expiration of objects in this bucket.

.. zuul:rolevar:: upload_image_s3_image_name
   :default: `{{ build_diskimage_image_name }}`

   The Zuul image name for use by zuul-launcher (e.g., `debian-bookworm`).

.. zuul:rolevar:: upload_image_s3_format

   The image format (e.g., `qcow2`).

.. zuul:rolevar:: upload_image_s3_extension
   :default: `{{ upload_image_s3_format }}`

   The extension to use when uploading (only used in the default
   values for the following variables.

.. zuul:rolevar:: upload_image_s3_filename
   :default: `{{ build_diskimage_image_root }}/{{ build_diskimage_image_name }}.{{ upload_image_s3_extension }}`

   The path of the local file to upload.

.. zuul:rolevar:: upload_image_s3_name
   :default: `{{ zuul.build }}-{{ build_diskimage_image_name }}.{{ upload_image_s3_extension }}`

   The object name to use when uploading.
