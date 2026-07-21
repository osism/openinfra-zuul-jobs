Run markdownlint against all markdown files in the given project.

**Role Variables**

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   Directory to search for markdown files in.

.. zuul:rolevar:: recurse
   :default: false

   Whether to recusively search for markdown files.
