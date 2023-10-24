LogJuicer Roles
===============

`LogJuicer <https://github.com/logjuicer/logjuicer>`_ extracts anomalies from log files.

You have two options to integrate LogJuicer in your Zuul job post-run phase:

#. Deploy the `web-service <https://github.com/logjuicer/logjuicer/tree/main/crates/web-service>`_ and use the :zuul:role:`report-logjuicer`.

#. Use the :zuul:role:`run-logjuicer` to create the report locally:

  * For single-node job, the role can be used in untrusted playbooks.
  * For multi-node job, the role must be used on localhost (the executor) between the :zuul:role:`fetch-output` and the log upload. Note that a future version may support merging reports produced on multi nodes through an untrusted playbooks.

In both case, a new artifact named "LogJuicer Report" will be provided to access the build report.

.. zuul:autorole:: report-logjuicer
.. zuul:autorole:: run-logjuicer
