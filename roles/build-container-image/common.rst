This is one of a collection of roles which are designed to work
together to build, upload, and promote container images in a gating
context:

* :zuul:role:`build-container-image`: Build the images.
* :zuul:role:`upload-container-image`: Upload the images to a registry.
* :zuul:role:`promote-container-image`: Promote previously uploaded images.

The :zuul:role:`build-container-image` role is designed to be used in
`check` and `gate` pipelines and simply builds the images.  It can be
used to verify that the build functions, or it can be followed by the
use of subsequent roles to upload the images to a registry.

The :zuul:role:`upload-container-image` role uploads the images to a
registry.  It can be used in one of two modes: by default it will
upload with a single tag corresponding to the change ID.  In this
mode, the role role is designed to be used in a job in a `gate`
pipeline so that the build produced by the gate is staged and can
later be promoted to production if the change is successful.  The
other mode allows for use of this job in a `release` pipeline to
directly upload a release build with the final set of tags.

The :zuul:role:`promote-container-image` role is designed to be used
in a `promote` pipeline.  It requires no nodes and runs very quickly
on the Zuul executor.  It simply re-tags a previously uploaded image
for a change with whatever tags are supplied by
:zuul:rolevar:`build-container-image.container_images.tags`.  It also
removes the change ID tag from the repository in the registry, and
removes any similar change ID tags.  This keeps the repository tidy in
the case that gated changes fail to merge after uploading their staged
images.

They all accept the same input data, principally a list of
dictionaries representing the images to build.  YAML anchors_ can be
used to supply the same data to all three jobs.

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

.. _anchors: https://yaml.org/spec/1.2/spec.html#&%20anchor//
