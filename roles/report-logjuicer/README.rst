Create a LogJuicer report link

This role emits an artifact to create a report through a LogJuicer web service.
Add the following task to your job post-run phase:

.. code-block:: yaml

   - when: not zuul_success | bool
     include_role:
       name: report-logjuicer
     vars:
       logjuicer_web_url: https://softwarefactory-project.io/logjuicer
       zuul_web_url: https://zuul.opendev.org/t/{{ zuul.tenant }}


**Role Variables**

.. zuul:rolevar:: logjuicer_web_url

   The http url of the LogJuicer web service.

.. zuul:rolevar:: zuul_web_url

   The http url of zuul-web.
   For multi-tenant deployment, add ``/t/{{ zuul.tenant }}``.
