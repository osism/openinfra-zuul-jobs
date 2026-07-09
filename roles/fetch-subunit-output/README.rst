Collect subunit outputs

**Role Variables**

.. zuul:rolevar:: zuul_work_dir
   :default: {{ ansible_user_dir }}/{{ zuul.project.src_dir }}

   Directory to work in. It has to be a fully qualified path.

.. zuul:rolevar:: fetch_subunit_output_additional_dirs
   :default: []

   List of additional directories which contains subunit files
   to collect. The content of zuul_work_dir is always checked,
   so it should not be added here.

.. zuul:rolevar:: fetch_subunit_output_artifact_name
   :default: Unit Test Report

   Name of the artifact entry returned to Zuul via ``zuul_return``.
   Override this when multiple jobs publish subunit results and you need
   distinct artifact labels in the build summary.

.. zuul:rolevar:: zuul_use_fetch_output
   :default: false

   Whether to synchronize files to the executor work dir, or to copy them
   on the test instance.
   When set to false, the role synchronizes the file to the executor.
   When set to true, the job needs to use the fetch-output role later.
