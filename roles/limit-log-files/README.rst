Limits log upload files based on number and size

This role checks that the log directory doesn't exceed a set number of files
or size limits per file pattern. If limits are violated, it registers the error
and reports a warning to Zuul.

**Role Variables**

.. zuul:rolevar:: limit_log_files_fail:
   :type: bool
   :default: false

   If set to true, the role will fail instead of reporting a warning to zuul.

.. zuul:rolevar:: limit_log_files_file_limit:
   :type: int
   :default: 100

   Maximum number of files allowed in the logs directory.

.. zuul:rolevar:: limit_log_files_file_rules:
   :type: string
   :default: see Example

   A list of file patterns and their size limits.
   The role calls the find command, which has specific file size constants, see `man find`.

   Example
   .. code-block:: yaml

      limit_log_files_file_rules:
         - ".*job-output.json$ 500k"
         - ".*\\zuul-manifest.json$ 1k"