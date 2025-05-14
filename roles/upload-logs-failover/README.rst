Upload logs to swift/s3/azure/... with a failover mechanism.

This role calls the ``upload-logs-[target]`` roles according to the list of
upload targets passed as role vars. If the current upload target fails, it
proceeds with the next item in its list until one of the uploads succeeded or
no more targets are available.

It expects the corresponding role vars of ``upload-logs-[target]`` to be
configured in the list of upload targets ``zuul_log_targets``. An example
configuration would look like the following and would ideally be passed as
a Zuul secret as it may hold passwords and access keys.

.. code-block:: yaml

    zuul_log_targets:
      - target: s3
        args:
          upload_logs_s3_endpoint: https://objectstore.example.com/
          zuul_log_bucket: log-bucket
          zuul_log_aws_access_key: foo
          zuul_log_aws_secret_key: bar
      - target: swift
        args:
          zuul_log_cloud_config:
            auth:
              username: foo
              password: bar
              user_domain_name: example
              auth_url: https://openstack.example.com:5000/v3/
          zuul_log_container: log-container

Requirements and dependencies of called ``upload-logs-[target]`` roles apply
accordingly, e.g. ``boto3`` for the s3 role. Please refer to their
corresponding documentation.

**Role Variables**

.. zuul:rolevar:: zuul_log_targets
   :type: list

   List of upload targets

.. zuul:rolevar:: zuul_log_targets.target
   :type: string

   Choice of "azure", "gcs", "s3", "swift", and any other platform specific
   "upload-logs-\*" role that might be availble.

.. zuul:rolevar:: zuul_log_targets.args
   :type: dict

   Complex argument which holds the variables required by the respective
   "upload-logs-\*" role specified by the "target" var. Please refer to their
   respective documentation.
