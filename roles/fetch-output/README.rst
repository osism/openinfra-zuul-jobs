Collect output from build nodes

This role collects logs, artifacts and docs from subdirs of the
``zuul_output_dir`` on the remote nodes to equivalent directories
on the executor so that later parts of the system can publish the
content to appropriate permanent locations.

.. note::

  Log content for multi-node jobs will be put into subdirectories
  based on remote node name. It is expected that artifacts and docs
  produced be inherently unique regardless of which build node they
  were produced on, so all artifacts and docs are pulled back to
  the same artifacts and docs directory.

**Role Variables**

.. zuul:rolevar:: fetch_output_rsync_bwlimit
   :default: (empty string, disabled)

   When set to a non-empty value, passes ``--bwlimit=VALUE`` to rsync
   to limit the transfer bandwidth. The value is in KiB/s
   (e.g. ``1000`` for ~1 MB/s).

.. zuul:rolevar:: fetch_output_rsync_human_readable
   :default: false

   When true, passes ``--human-readable`` to rsync to display numbers
   in human-readable format (e.g. KB, MB) instead of raw bytes.

.. zuul:rolevar:: fetch_output_rsync_log_file
   :default: false

   When true, passes ``--log-file`` to rsync to save the transfer
   listing to ``fetch-output.log`` in the logs directory. Useful
   in combination with ``fetch_output_rsync_quiet`` to suppress
   entries in ``job-output.txt`` while still keeping a record
   of the transferred files.

.. zuul:rolevar:: fetch_output_rsync_no_motd
   :default: false

   When true, passes ``--no-motd`` to rsync to suppress the daemon
   message of the day.

.. zuul:rolevar:: fetch_output_rsync_quiet
   :default: false

   When true, passes ``--quiet`` to rsync to suppress the per-file
   transfer listing. Useful when collecting large numbers of files.
   Any warnings and transfer errors are still printed.

.. zuul:rolevar:: fetch_output_rsync_stats
   :default: false

   When true, passes ``--stats`` to rsync to print a transfer summary
   (bytes sent/received, number of files, total size, etc.).

.. zuul:rolevar:: fetch_output_rsync_timeout
   :default: 0

   Sets the I/O timeout in seconds for rsync. A value of 0 means
   no timeout. If no data is transferred for the specified time,
   rsync will exit.

.. zuul:rolevar:: zuul_output_dir
   :default: {{ ansible_user_dir }}/zuul-output

   Base directory for collecting job output.
