By default configures the inventory hostnames in a multi-node job resolve
to their respective private ipv4 addresses through the /etc/hosts file on
each node.

If you set use_private_ip_addresses to false then this role will configure
/etc/hosts using public ipv4 addresses instead.
