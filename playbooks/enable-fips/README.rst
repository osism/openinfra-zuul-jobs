The enable-fips playbook can be invoked to enable FIPS mode on jobs.

This playbook will call the enable-fips role, which will turn FIPS mode on
and then reboot the node.  To get consistent results, this role should
be run very early in the node setup process, so that resources set up
later are not affected by the reboot.

A playbook variable enable_fips - which defaults to True - is provided.
This variable can be used to skip this playbook.

**Job Variables**

.. zuul:jobvar:: enable_fips
   :default: True

   Whether to run the playbook and enable fips.  Defaults to True.


