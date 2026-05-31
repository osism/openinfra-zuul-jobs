Install podman container manager

**Role Variables**

.. zuul:rolevar:: ensure_podman_validate
   :default: false

   Used to enable validation of podman engine.

.. zuul:rolevar:: ensure_podman_socket
   :default: false

   Enabling this will cause the role to configure a group and add the
   user to it in order to have access to the root-owned system-level
   compatability socket.

.. zuul:rolevar:: ensure_podman_group
   :default: podman

   Only used if `ensure_podman_socket` is set.  Configures the group
   name to use.

.. zuul:rolevar:: ensure_podman_rootless
   :default: false

   Configure Podman for rootless operation.  This installs the rootless
   networking package set and configures the Ansible user with subordinate
   UID/GID ranges and a user containers.conf using pasta and netavark.

   This is currently supported on Ubuntu 24.04, Ubuntu 26.04, Debian
   Bookworm, and Debian Trixie.  The role will fail if this is enabled on an
   unsupported platform.

.. zuul:rolevar:: ensure_podman_rootless_unprivileged_port_start
   :default: null

   When rootless mode is enabled, set
   ``net.ipv4.ip_unprivileged_port_start`` to this value.  For example,
   set this to ``80`` to allow unprivileged users to bind ports 80 and
   higher.

.. zuul:rolevar:: ensure_podman_rootless_subuid_start
   :default: 100000

   Start of the subordinate UID range configured for the Ansible user when
   rootless mode is enabled.

.. zuul:rolevar:: ensure_podman_rootless_subuid_count
   :default: 65536

   Size of the subordinate UID range configured for the Ansible user when
   rootless mode is enabled.

.. zuul:rolevar:: ensure_podman_rootless_subgid_start
   :default: 100000

   Start of the subordinate GID range configured for the Ansible user when
   rootless mode is enabled.

.. zuul:rolevar:: ensure_podman_rootless_subgid_count
   :default: 65536

   Size of the subordinate GID range configured for the Ansible user when
   rootless mode is enabled.

.. zuul:rolevar:: podman_compose_install
   :default: false

   Install ``podman-compose`` in addition to Podman.
