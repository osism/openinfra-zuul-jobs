Mirror the local git repos to remote nodes

This role uses either rsync or git operations to mirror the locally
prepared git repos to the remote nodes while taking advantage of
cached repos on the node if they exist.  This role works generically
regardless of the existence of a cached repo on the node.

If a repo or cache exists on the remote node, the role will use git
operations in order to most quickly transfer the least amount of data.
If no remote repo or cache exists, the role will use rsync for speed
and memory efficiency.

This role will work with either SSH or kubectl connections.  Note that
if rsync is used with an SSH connection, the persistent SSH connection
managed by Ansible is not used and a new SSH connection will be
established for each repo that is synchronized.

The cached repos need to be placed using the canonical name under the
`cached_repos_root` directory.

**Role Variables**

.. zuul:rolevar:: cached_repos_root
   :default: /opt/git

   The root of the cached repos.

.. zuul:rolevar:: prepare_repos_sync_required_projects_only
   :type: bool
   :default: False

   A flag which if set to true, filters the list of projects to be
   synchronized to include only projects which are required by the
   job.

.. zuul:rolevar:: zuul_workspace_root
   :default: "{{ ansible_user_dir }}"

   The root of the workspace in which the repos are mirrored.
