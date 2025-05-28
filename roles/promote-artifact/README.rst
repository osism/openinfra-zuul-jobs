Promote artifacts from a completed build of a Zuul job

Given a change, this role returns artifacts from a previous build (by
default, a build of the current change).  It simply returns the same
artifact metadata that matches the supplied artifact type without
transferring any artifact data.


**Role Variables**

.. zuul:rolevar:: promote_artifact_api

   The Zuul API endpoint to use.  Example: ``https://zuul.example.org/api/tenant/{{ zuul.tenant }}``

.. zuul:rolevar:: promote_artifact_pipeline

   The pipeline in which the previous build ran.

.. zuul:rolevar:: promote_artifact_job

   The job of the previous build.

.. zuul:rolevar:: promote_artifact_type

   The artifact type.  This is the value of the ``type`` field in the
   artifact metadata. This can be a string or a list of strings.

.. zuul:rolevar:: promote_artifact_query
   :default: change={{ zuul.change }}&patchset={{ zuul.patchset }}&pipeline={{ promote_artifact_pipeline }}&job_name={{ promote_artifact_job }}

   The query to use to find the build.  Normally the default is used.
