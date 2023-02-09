Enable FIPS on a node.

Set a node into FIPS mode, to test functionality when crypto
policies are set to FIPS in RHEL/Centos >=8 or Ubuntu.

For Ubuntu nodes, the node is assumed to already have an Ubuntu
Advantage subscription activated, as this is required to enable
FIPS mode.  The enable-ua-subscription role in this repo can be
used to activate the subscription.

The role will set the node into FIPS mode, reboot the node, and
then call the post-reboot-tasks role.  This role requires a role
parameter - nslookup_target.
