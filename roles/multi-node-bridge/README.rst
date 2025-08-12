.. warning::
   This role currently depends on openvswitch and the now deprecated by
   Ansible openvswitch_bridge module. This transitively means this role is
   effectively deprecated as well. In order to get around the deprecation
   and removal of this Ansible module we have vendored it in this role. This
   may not work with future versions of Ansible

   Ideally we would rewrite the role to use Linux bridges instead of
   openvswitch as this set of tooling is more readily available and common
   on Linux machines. We could continue to use VXLAN with Linux bridge or
   consider switching to GENEVE or maybe even Wireguard as alternative
   overlay methods during that switch.

   Help is very much appreciated to make this rewrite happen.

Configures a VXLAN virtual network overlay through an openvswitch network
bridge between a 'switch' node and 'peer' nodes.

This allows members of the bridge to communicate with each other through the
virtual network.

By default, this role will:

- Install and start ``openvswitch``
- Set up a ``br-infra`` bridge on all nodes
- Set up the connectivity between the switch and the peer with a virtual port
- Set up an ip address on the bridge interface:

::

    172.24.4.1/23 # switch node
    172.41.4.2/23 # first peer
    172.41.4.3/23 # second peer
    ...

**Role requirements**

This role requires and expects two groups to be set up in the Ansible host
inventory in order to work:

- ``switch`` (the node acting as the switch)
- ``peers`` (nodes connected to the virtual switch ports)

**Role variables**

.. zuul:rolevar:: bridge_vni_offset
   :default: 1000000

   VXLAN Network Identifier offset (openvswitch key).

.. zuul:rolevar:: bridge_mtu
   :default: Smallest mtu less 50 bytes for vxlan overhead

   Bridge interface MTU. By default we determine this value by checking
   all interfaces on host, taking the smallest MTU and subtracting by
   50 for vxlan overhead. Can be overridden explicitly if this does not
   work.

.. zuul:rolevar:: bridge_name
   :default: br-infra

   Name of the bridge interface.

.. zuul:rolevar:: bridge_configure_address
   :default: true

   Whether or not to configure an IP address on the bridge interface.

.. zuul:rolevar:: bridge_authorize_internal_traffic
   :default: false

   When ``bridge_configure_address`` is ``true``, whether or not to set up
   firewall rules to allow traffic freely within the bridge
   subnet (``bridge_address_prefix``.0/``bridge_address_subnet``).

.. zuul:rolevar:: bridge_address_prefix
   :default: 172.24.4

   The IP address range prefix.

.. zuul:rolevar:: bridge_address_offset
   :default: 1

   The IP address offset, used with ``bridge_address_prefix`` to provide the
   full IP address. The initial offset defines the IP address of the switch
   node in the virtual network.

.. zuul:rolevar:: bridge_address_subnet
   :default: 23

   The IP address range CIDR/subnet.

.. zuul:rolevar:: install_ovs
   :default: true

   Whether or not to install openvswitch. It can be set to false
   when ovs installation is taken care outside of the role.
