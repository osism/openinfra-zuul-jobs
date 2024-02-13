Run the zuul-admin tenant-conf-check command.

This requires a partial zuul.conf (it only needs the connection
entries, and those without any credential information) and a tenant
config file.  It will validate the syntax of the tenant config file
(but not the job configuration of any projects in the tenants).

**Role Variables**

.. zuul:rolevar:: zuul_tenant_conf_check_zuul_conf_path

   The path to the partial zuul.conf to use.  This must contain the
   connection entries, but no credentials are required.  Any other
   sections are ignored.

.. zuul:rolevar:: zuul_tenant_conf_check_tenant_config_path

   The path to the tenant config file to check.

.. zuul:rolevar:: zuul_tenant_conf_check_image
   :default: quay.io/zuul-ci/zuul-scheduler:latest

   The Zuul scheduler container image which contains the zuul-admin
   command to run.

.. zuul:rolevar:: zuul_tenant_conf_check_registry_credentials

   An optional value, expected in the form of a secret, that supplies
   credential information if zuul_tenant_conf_check_image is in a
   registry that requires authentication.  The format is a dictionary
   keyed by the registry name.  Example:

   .. code-block:: yaml

      zuul_tenant_conf_check_registry_credentials:
        docker.io:
          username: 'username'
          password: 'password'

   .. zuul:rolevar:: [registry_name]

      The dictionary key should be the name of the registry

      .. zuul:rolevar:: username

         The registry username.

      .. zuul:rolevar:: password

         The registry password.
