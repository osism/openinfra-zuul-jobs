Runs a container registry for the use of this buildset.

This may be used for a single job running on a single node, or it may
be used at the root of a job graph so that multiple jobs running for a
single change can share the registry.

**Role Variables**

.. zuul:rolevar:: buildset_registry_image
   :default: quay.io/zuul-ci/zuul-registry:latest

   Container image used to launch the buildset registry.

.. zuul:rolevar:: buildset_registry_root
   :default: {{ ansible_user_dir }}/buildset_registry

   Path for the registry volumes.

.. zuul:rolevar:: buildset_registry_port
   :default: 5000

   The port on which the registry should listen.

.. zuul:rolevar:: container_command
   :default: docker

   The command to use to run the registry container (E.g., ``podman``).


**Return Values**

.. zuul:rolevar:: buildset_registry

   Information about the registry.

   .. zuul:rolevar:: host

      The host (IP address) of the registry.

   .. zuul:rolevar:: port

      The port on which the registry is listening.

   .. zuul:rolevar:: username

      The username used to access the registry via HTTP basic auth.

   .. zuul:rolevar:: password

      The password used to access the registry via HTTP basic auth.

   .. zuul:rolevar:: cert

      The (self-signed) certificate used by the registry.
