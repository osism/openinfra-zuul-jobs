This is one of a collection of jobs which are designed to work
together to build, upload, and promote container images in a gating
context:

  * :zuul:job:`build-container-image`: Build the images.
  * :zuul:job:`upload-container-image`: Build and stage the images in a registry.
  * :zuul:job:`promote-container-image`: Promote previously uploaded images.

The jobs can work in multiple modes depending on your requirements.
They all accept the same input data, principally a list of
dictionaries representing the images to build.  YAML anchors_ can be
used to supply the same data to all three jobs.

*Promotion via tags*

The :zuul:job:`build-container-image` job runs in the `check` pipeline
to validate the change.

The :zuul:job:`upload-container-image` job runs in the `gate` pipeline
and builds and uploads the images to a remote registry, but only with
a single temporary tag corresponding to the change ID.  This is a
*speculative* upload; the change is not "live" (the main tag is not
updated) and other gate jobs may fail and the change may not merge,
effectively invalidating the upload.

The :zuul:job:`promote-container-image` job runs in a post-merge
`promote` pipeline.  It requires no nodes and runs very quickly on the
Zuul executor.  It simply re-tags a previously uploaded image for a
change with whatever tags are supplied by
:zuul:jobvar:`build-container-image.container_images.tags` after the
code has merged.  It also cleans up and removes the change ID tag from
the repository in the registry.  If any changes fail to merge, this
cleanup will not run and those tags will need to be deleted manually.

This advantage of this method is that it minimises the window in which
the published image differs from the merged code.  There are some
caveats to be aware of. `gate` failures may mean that unused layers
and tags are present in the remote repository, which need to be
cleaned up.  Removing registry tags is not a generic option; you will
need to check the promote role documentation to ensure you are passing
the right registry details so tags can be cleaned up.

In the `tag` and `release` pipelines there is no need for a
speculative upload (the tagged/released change is committed code and
has already passed gate tests).  In this case,
:zuul:job:`upload-container-image` job is run with the flag
``upload_container_image_promote: false`` to directly build and push
with the final tags.

Summary:

* :zuul:job:`build-container-image` in `check`
* :zuul:job:`upload-container-image` in `gate`
* :zuul:job:`promote-container-image` in `promote` with
  ``promote_container_method: tag``
* :zuul:job:`upload-container-image` with
  ``upload_container_image_promote: false`` in `tag` and `release`

*Promotion via intermediate registry*

The :zuul:job:`build-container-image` runs in the `check` pipeline.
It will build images then upload them to an intermediate registry.

The :zuul:job:`upload-container-image` job  runs in the `gate`. With
this promotion method it will build and upload images to an intermediate
registry. No images will be pushed to the upstream registry until
promotion occurs.

The :zuul:job:`promote-container-image` job is designed to be used in
a post-merge `promote` pipeline.  It requires no nodes and run on the
Zuul executor.  It inspects the artifacts of the gate job to find the
correct tags to pull from the intermediate registry.  It then uploads
this image from the intermediate registry to the remote registry with
the final tags supplied by
:zuul:jobvar:`build-container-image.container_images.tags`.

In the `tag` and `release` pipelines the
:zuul:job:`upload-container-image` job is run with the flag
``upload_container_image_promote: false`` to directly build and push
with the final tags.

The advantages of this method is that no partial or unused images will
ever be present in the final repository.  Copying from the
intermediate registry effectively caches the expensive build process.
This means that although the window that the production tags are
out-of-sync with the merged code is larger than when using speculative
uploads, it is smaller than having to rebuild *and* upload the image.
Copying is a generic operation, so it should work with any registry.
The layer upload has more exposure to transient errors than the
``tag`` promotion step, so needs to be monitored more carefully.  You
also must manage an external intermediate registry to hold the image
between upload and promote steps in this model.

Summary:

* :zuul:job:`build-container-image` in `check`
* :zuul:job:`upload-container-image` in `gate`.  This must push to an
  intermediate registry.
* :zuul:job:`promote-container-image` in `promote` with
  ``promote_container_method: intermediate-registry``
* :zuul:job:`upload-container-image` with
  ``upload_container_image_promote: false`` in `tag` and `release`

*Publish via full release*

The :zuul:job:`build-container-image` job runs in the `check` pipeline
to validate the change.

The :zuul:job:`build-container-image` job also runs in the `gate`
pipeline to validate the change before merge.

Once the change has merged, :zuul:job:`upload-container-image` job is
run with the flag ``upload_container_image_promote: false`` to
directly build and push with the final tags.  This is also run in the
`tag` and `release` piplines in the same way.

The advantage of this mode is that it requires no external
dependencies or management of speculative uploads.  The disadvantage
is that it has the longest window where published image is out-of-sync
with merged-code, as the post-merge release process must re-build the
entire container and upload it.

* :zuul:job:`build-container-image` in `check`
* :zuul:job:`build-container-image` in `gate`
* :zuul:job:`upload-container-image` with
  ``upload_container_image_promote: false`` after code merge, and
  `tag` and `release` pipelines.

**Job Variables**

.. zuul:jobvar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   The project directory.  Serves as the base for
   :zuul:jobvar:`build-container-image.container_images.context`.

.. zuul:jobvar:: container_filename

   The default container filename name to use. Serves as the base for
   :zuul:jobvar:`build-container-image.container_images.container_filename`.
   This allows a global overriding of the container filename name, for
   example when building all images from different folders with
   similarily named containerfiles.

   If omitted, the default depends on the container command used.
   Typically, this is ``Dockerfile`` for ``docker`` and
   ``Containerfile`` (with a fallback on ``Dockerfile``) for
   ``podman``.

.. zuul:jobvar:: container_command
   :default: podman

   The command to use when building the image (E.g., ``docker``).

.. zuul:jobvar:: container_images
   :type: list

   A list of images to build.  Each item in the list should have:

   .. zuul:jobvar:: context

      The build context; this should be a directory underneath
      :zuul:jobvar:`build-container-image.zuul_work_dir`.

   .. zuul:jobvar:: container_filename

      The filename of the container file, present in the context
      folder, used for building the image. Provide this if you are
      using a non-standard filename for a specific image.

   .. zuul:jobvar:: registry

      The name of the target registry (E.g., ``quay.io``).  Used by
      the upload and promote roles.

   .. zuul:jobvar:: repository

      The name of the target repository in the registry for the image.
      Supply this even if the image is not going to be uploaded (it
      will be tagged with this in the local registry).  This should
      include the registry name.  E.g., ``quay.io/example/image``.

   .. zuul:jobvar:: path

      Optional: the directory that should be passed to the build
      command.  Useful for building images with a container file in
      the context directory but a source repository elsewhere.

   .. zuul:jobvar:: build_args
      :type: list

      Optional: a list of values to pass to the ``--build-arg``
      parameter.

   .. zuul:jobvar:: target

      Optional: the target for a multi-stage build.

   .. zuul:jobvar:: tags
      :type: list
      :default: ['latest']

      A list of tags to be added to the image when promoted.

   .. zuul:jobvar:: siblings
      :type: list
      :default: []

      A list of sibling projects to be copied into
      ``{{zuul_work_dir}}/.zuul-siblings``.  This can be useful to
      collect multiple projects to be installed within the same Docker
      context.  A ``-build-arg`` called ``ZUUL_SIBLINGS`` will be
      added with each sibling project.  Note that projects here must
      be listed in ``required-projects``.

.. zuul:jobvar:: container_build_extra_env
   :type: dict

   A dictionary of key value pairs to add to the container build environment.
   This may be useful to enable buildkit with docker builds for example.

.. _anchors: https://yaml.org/spec/1.2/spec.html#&%20anchor//
