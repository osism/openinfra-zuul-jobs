Ensure that processes are running after a node reboot.

Some roles (like the enable-fips role) need to reboot the node
in order to complete their operations.

This role can be invoked to ensure that the node is sufficiently
up again before continuing by doing some basic checks for
connectivity (ssh), restarting the zuul-console and making sure
DNS is up.

A role parameter nslookup_target is required to specify the DNS name
to ensure DNS is working.

**Role Variables**

.. zuul:rolevar:: nslookup_target
   :type: str
   :default: None

   DNS name to query to confirm that DNS is working.  If working in a
   mirrored environment, it is a good idea to use $zuul_site_mirror_fqdn,
   because this is what will be needed for package installs in any case.
