Ensure zookeeper is running

Install and start zookeeper using the upsteam release.

**Role Variables**

.. zuul:rolevar:: zookeeper_version
   :default: latest

   The zookeeper version.

.. zuul:rolevar:: zookeeper_use_tls
   :default: false

   Setup zookeeper tls certificates.

.. zuul:rolevar:: zookeeper_use_tmpfs
   :default: true

   Setup a tmpfs for data directory.

.. zuul:rolevar:: zookeeper_use_eatmydata
   :default: false

   Uses "eatmydata" so that fsync returns immediately.  May be useful
   for testing, but never use this in production.
