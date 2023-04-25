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
   This application API token needs create permissions. If the registry
   name is quay.io we know that the registry type is ``quay``. If you are
   running a private Quay installation you can manually set
   ``type`` to ``quay`` to force this behavior.

   This role will only take action on image repos that map to
   container registries for which both an ``api_token`` is set and
   ``type`` can be determined to be ``quay``.

   You may also set ``api_url`` on the registry credentials if the
   API is not hosted at the root of the registry name. Most installations
   should be able to ignore this and use the default of
   ``https://{{ $name }}``.

   Example:

   .. code-block:: yaml

      container_registry_credentials:
        quay.io:
          type: 'quay'
          api_token: 'abcd1234'
          api_url: 'https://quay.io'

.. zuul:rolevar:: container_images
   :type: list

   Required. A list of dictionaries. This provides info about the image
   repositories to be created in a quay registry. For convenience this
   is in the same format as the ``container_images`` variable used by other
   container roles. Specify a ``registry`` (this should match up with your
   credentials to locate the api token), ``namespace``, ``repo_shortname``,
   ``repo_description``, and ``visibility`` attributes. By default
   visibility will be ``public``.

   Example:

   .. code-block:: yaml

      container_images:
        - registry: quay.io
          namespace: myquayorg
          repo_shortname: myimage
          repo_description: The best container image
