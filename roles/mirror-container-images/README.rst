Copy container images from one registry to another.

.. zuul:rolevar:: mirror_container_images_images
   :type: list

   A list of container images to copy.

   .. zuul:rolevar:: src_repository
      :type: str

      The source image repository (including registry name).

   .. zuul:rolevar:: src_tag
      :type: str

      The source image tag.

   .. zuul:rolevar:: dest_repository
      :type: str

      The destination image repository (including registry name).

   .. zuul:rolevar:: dest_tag
      :type: str

      The destination image tag.

   .. zuul:rolevar:: dest_registry
      :type: str

      The name of the registry to which the destination image will be
      pushed.

.. zuul:rolevar:: container_registry_credentials
   :type: dict

   This is expected to be a Zuul Secret in dictionary form.  Each key
   is the name of a registry, and its value a dictionary with
   information about that registry.

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

