Remove tags from registry

This role creates a generic interface for removing tags from a
container registry.  The OCI distribution API (implemented essentially
all registries) does specify a tag deletion endpoint, but as at
2023-03 essentially no registries implement it.  This means
practically we must talk to the per-registry API directly to remove
tags.  The methods to delete tags are generally similar across
registries, but differ slightly in endpoint names, etc.

This role can run in two modes; either removing a single specific tag,
or it can run a cleanup process removing all tags that match a given
prefix and have not been modified in a given amount of time.

For public registries this role should guess the API from the
repository name.  If you are running against a private registry, you
will need to explicitly specify the API type and URL prefix to
communicate to using arguments below.

**Role Variables**

.. zuul:rolevar:: remove_registry_tag_repository
   :type: string

   Required.  This must be the full repository;
   e.g. ``quay.io/organisation/image``

.. zuul:rolevar:: container_registry_credentials
   :type: dict

   Required.  This is expected to be a Zuul secret in dictionary form.
   For convenience this is in the same format as the
   ``container_registry_credentials`` variable used by the other
   container roles.  You must specify the correct variables for the
   registry you are communicating with:

   * **quay.io** : Specify an ``api_key`` which is issued from an
     application assigned to an organisation.  See
     `<https://docs.quay.io/api/>`__
   * **docker.io** : Username and password

   Example:

   .. code-block:: yaml

      container_registry_credentials:
        quay.io:
          api_token: 'abcd1234'
        docker.io:
          username: 'username'
          password: 'password'

.. zuul:rolevar:: remove_registry_tag_tag
   :type: string

   Optional.  If set, the specific tag to remove.

.. zuul:rolevar:: remove_registry_tag_regex
   :type: string
   :default: '^change_.*$|^{{ zuul.pipeline }}_.*$'

   Optional.  If
   :zuul:rolevar:`remove-registry-tag.remove_registry_tag_tag` is
   unset, any tags matching this regex *and* exceeding the age in
   :zuul:rolevar:`remove-registry-tag.remove_registry_tag_age` will be
   removed.  The default is tags matching those created by the promote
   upload roles.

.. zuul:rolevar:: remove_registry_tag_age
   :type: int
   :default: 86400

   Optional.  The age, in seconds, a tag that matches
   :zuul:rolevar:`remove-registry-tag.remove_registry_tag_regex`
   last-modified timestamp must exceed to be removed.

.. zuul:rolevar:: remove_registry_tag_api_type
   :type: string

   Optional.  By default the role will guess the API type from the
   repository name.  However, if you need to override this choice
   specify one of:

   * quay
   * docker

.. zuul:rolevar:: remove_registry_tag_api_url
   :type: string

   Optional.  This role will use the default URL for the given
   registry API.  If you need to override this choice, specify this
   variable.
