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
