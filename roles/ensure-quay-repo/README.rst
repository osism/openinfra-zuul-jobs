This role primarily exists to create a new public repository in quay.
This role can be used to create private repos as well, but repos are
created by default in quay if you simply push to them.

Users of this role will need to generate an application token with
`create repository` permissions. Additional permissions are not
necessary.

When invoking this role you should set no_log: true on the
`include_role` task to prevent disclosure of your token.

** Role Variables **

.. zuul:rolevar:: container_registry_credentials
   :type: dict

   Required.  This is expected to be a Zuul secret in dictionary form.
   For convenience this is in the same format as the
   ``container_registry_credentials`` variable used by the other container
   roles. Specify an ``api_token`` which is issued from an application
   assigned to an organisation.  See `<https://docs.quay.io/api/>`__

   Example:

   .. code-block:: yaml

      container_registry_credentials:
        quay.io:
          api_token: 'abcd1234'

.. zuul:rolevar:: container_images
   :type: list

   Required. A list of dictionaries. This provides info about the image
   repositories to be created in a quay registry. For convenience this
   is in the same format as the ``container_images`` variable used by other
   container roles. Specify a ``registry`` (this should match up with your
   credentials to locate the api token), ``namespace``, ``repo_shortname``,
   ``repo_description``, ``visibility``, and ``api_url`` attributes.

   By default visibility will be ``public`` and ``api_url`` will be
   ``https://{{ registry }}``.

   Example:

   .. code-block:: yaml

      container_images:
        - registry: quay.io
          namespace: myquayorg
          repo_shortname: myimage
          repo_description: The best container image
