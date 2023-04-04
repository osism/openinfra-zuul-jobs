This is one of a collection of roles which are designed to work
together to build, upload, and promote container images in a gating
context:

* :zuul:role:`build-container-image`: Build the images.
* :zuul:role:`upload-container-image`: Upload the images to a registry.
* :zuul:role:`promote-container-image`: Promote previously uploaded images.

All roles accept the same input data, principally a list of
dictionaries representing the images to build.  YAML anchors_ can be
used to supply the same data to all three roles.

*Building*

The :zuul:role:`build-container-image` role is designed to be used in
`check` and `gate` pipelines and simply builds the images.  It can be
used to verify that the build functions, or it can be followed by the
use of subsequent roles to upload the images to a registry.

*Uploading*

The :zuul:role:`upload-container-image` role uploads the images to a
registry.  It can be used in one of two modes:

1. The default mode is as part of a two-step `promote` pipeline.  This
   mode is designed to minimize the time the published registry tag is
   out of sync with the changes Zuul has merged to the underlying code
   repository.

   In this mode, the role is intended to run in the `gate` pipeline.
   Zuul will build and upload the resulting image with a single tag
   prefixed with the change ID (e.g. ``change_12345_<tag>``).  Thus at
   the completion of the `gate` job, all the layers of the new
   container are uploaded, but the ``<tag>`` in the remote repository
   will not have been updated.

   Once the gate queue is successfully finished Zuul will merge the
   change to the code-repository.  At this point, a small window opens
   where the ``<tag>`` is pointing to a container that does not
   reflect the state of the code-repository.  The merge of the change
   will trigger the `promote` pipeline which uses a very quick,
   executor-only job to retag ``<tag>`` to ``change_12345_<tag>``.
   Since this step does not require any nodes or upload any data, it
   generally takes only a few seconds.  The remote container pointed
   to by ``<tag>`` will now reflect the underlying code closing the
   out-of-sync window.

2. The other mode allows for use of this job in a `release` pipeline
   to directly upload a release build with the final set of tags.

   In this mode, the completion of the `gate` jobs will have merged
   the code changes, and the role will now have to build and upload
   the resulting image to the remote repository.  Once uploaded, the
   tags will be updated.

   The alternative `promote` method can be thought of as a
   "speculative" upload.  There is a possibility the `gate` job
   uploads layers and creates a temporary tag, but either the
   container upload or another co-gating job fails, causing the `gate`
   jobs to fail overall.  This causes extra uploads, unsued layers and
   unused tags that require cleaning up.  Since changes have merged
   before the `release` pipeline starts, the upload will simply not
   run if the gate jobs fail.  This avoids uploading or tagging
   anything that will not be used.  The trade-off is a higher latency
   between merging code and publishing final tags.

   Transient network failures can cause upload errors in both cases.
   Although the `promote` job may fail, leaving the tag incorrectly
   unmodified, the `promote` job's relatively simplicity minimises
   potential error.  The `release` pipeline does more work, exposing
   it to a higher chance of failures such as transient network errors
   etc., also resulting in the repository tag being out-of-date.  In
   both cases developers must pay close attention as failures in these
   pipelines are often less noticable than code not merging with a
   gate-job failure.

*Promoting*

As discussed above, the :zuul:role:`promote-container-image` role is
designed to be used in a `promote` pipeline.  It re-tags a previously
uploaded image by copying the temporary change-id based tags made
during upload to the final production tags supplied by
:zuul:rolevar:`build-container-image.container_images.tags`.  It is
intended to run very quickly and with no dependencies, so it can run
directly on the Zuul executor.

Once this role completes, the temporary upload tags are no longer
required.  The role removes the change-id tags from the repository in
the registry, and removes any similar change-ids tags.  This keeps the
repository tidy in the case that gated changes fail to merge after
uploading their staged images.

*Dependencies*

Use the :zuul:role:`ensure-skopeo` role as well as the
:zuul:role:`ensure-docker`, or :zuul:role:`ensure-podman` roles before
using the roles described here.

**Role Variables**

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   The project directory.  Serves as the base for
   :zuul:rolevar:`build-container-image.container_images.context`.

.. zuul:rolevar:: container_filename

   The default container filename name to use. Serves as the base for
   :zuul:rolevar:`build-container-image.container_images.container_filename`.
   This allows a global overriding of the container filename name, for
   example when building all images from different folders with
   similarily named containerfiles.

   If omitted, the default depends on the container command used.
   Typically, this is ``Dockerfile`` for ``docker`` and
   ``Containerfile`` (with a fallback on ``Dockerfile``) for
   ``podman``.

.. zuul:rolevar:: container_command
   :default: podman

   The command to use when building the image (E.g., ``docker``).

.. zuul:rolevar:: container_registry_credentials
   :type: dict

   This is only required for the upload and promote roles.  This is
   expected to be a Zuul Secret in dictionary form.  Each key is the
   name of a registry, and its value a dictionary with information
   about that registry.

   Example:

   .. code-block:: yaml

      container_registry_credentials:
        quay.io:
          username: foo
          password: bar

   .. zuul:rolevar:: [registry name]
      :type: dict

      Information about a registry.  The key is the registry name, and
      its value a dict as follows:

      .. zuul:rolevar:: username

         The registry username.

      .. zuul:rolevar:: password

         The registry password.

      .. zuul:rolevar:: repository

         Optional; if supplied this is a regular expression which
         restricts to what repositories the image may be uploaded.  The
         following example allows projects to upload images to
         repositories within an organization based on their own names::

           repository: "^myorgname/{{ zuul.project.short_name }}.*"

.. zuul:rolevar:: container_images
   :type: list

   A list of images to build.  Each item in the list should have:

   .. zuul:rolevar:: context

      The build context; this should be a directory underneath
      :zuul:rolevar:`build-container-image.zuul_work_dir`.

   .. zuul:rolevar:: container_filename

      The filename of the container file, present in the context
      folder, used for building the image. Provide this if you are
      using a non-standard filename for a specific image.

   .. zuul:rolevar:: registry

      The name of the target registry (E.g., ``quay.io``).  Used by
      the upload and promote roles.

   .. zuul:rolevar:: repository

      The name of the target repository in the registry for the image.
      Supply this even if the image is not going to be uploaded (it
      will be tagged with this in the local registry).  This should
      include the registry name.  E.g., ``quay.io/example/image``.

   .. zuul:rolevar:: path

      Optional: the directory that should be passed to the build
      command.  Useful for building images with a container file in
      the context directory but a source repository elsewhere.

   .. zuul:rolevar:: build_args
      :type: list

      Optional: a list of values to pass to the ``--build-arg``
      parameter.

   .. zuul:rolevar:: target

      Optional: the target for a multi-stage build.

   .. zuul:rolevar:: tags
      :type: list
      :default: ['latest']

      A list of tags to be added to the image when promoted.

   .. zuul:rolevar:: siblings
      :type: list
      :default: []

      A list of sibling projects to be copied into
      ``{{zuul_work_dir}}/.zuul-siblings``.  This can be useful to
      collect multiple projects to be installed within the same Docker
      context.  A ``-build-arg`` called ``ZUUL_SIBLINGS`` will be
      added with each sibling project.  Note that projects here must
      be listed in ``required-projects``.

.. zuul:rolevar:: container_build_extra_env
   :type: dict

   A dictionary of key value pairs to add to the container build environment.
   This may be useful to enable buildkit with docker builds for example.

.. _anchors: https://yaml.org/spec/1.2/spec.html#&%20anchor//
