Create a LogJuicer report

This role runs the `LogJuicer <https://github.com/logjuicer/logjuicer>`_ tool
to create a report of the current build.
For single-node jobs, the role can be used on the test instance in the job post-run phase.

.. code-block:: yaml

   - when: not zuul_success | bool
     include_role:
       name: run-logjuicer
     vars:
       zuul_web_url: https://zuul.opendev.org/

For multi-node jobs, the role must be used on localhost (the executor)
between the :zuul:role:`fetch-output` and the log upload.


**Role Variables**

.. zuul:rolevar:: zuul_web_url

   The zuul-web URL, to lookup baselines.

.. zuul:rolevar:: logjuicer_max_run_time
   :default: 900

   Maximum runtime in seconds.
