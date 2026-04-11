# Copyright 2024-2026 Acme Gating, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import time
import shlex
from tempfile import NamedTemporaryFile

from ansible.module_utils.basic import AnsibleModule

try:
    # Ansible context
    from ansible.module_utils.zuul_jobs.prepare_repos_utils import (
        run,
        for_each_project,
    )
except ImportError:
    # Test context
    from ..module_utils.zuul_jobs.prepare_repos_utils import (
        run,
        for_each_project,
    )


def get_ssh_dest(args, dest):
    return (
        "git+ssh://%s@%s:%s/%s" % (
            args['ansible_user'],
            args['ansible_host'],
            args['ansible_port'],
            dest)
    )


def get_k8s_dest(args, dest):
    resources = args['zuul_resources'][args['inventory_hostname']]
    return (
        "\"ext::kubectl --context %s -n %s exec -i %s -- %%S %s\"" % (
            resources['context'],
            resources['namespace'],
            resources['pod'],
            dest)
    )


def get_rsync_dest(args, dest):
    return args['ansible_host'] + ":" + dest


class KubectlRsh:
    def __init__(self, resource):
        self.resource = resource

    def __enter__(self):
        self.file = NamedTemporaryFile(delete=False)
        self.file_exit = self.file.__enter__()
        # This wrapper script is required because kubectl wants a "--"
        # after the host and rsh doesn't.
        cmd = 'shift;kubectl --context %s --namespace %s exec -i %s -- $@' % (
            shlex.quote(self.resource['context']),
            shlex.quote(self.resource['namespace']),
            shlex.quote(self.resource['pod']),
        )
        self.file.write(cmd.encode('utf8'))
        self.file.close()
        os.chmod(self.file.name, 0o755)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.file_exit.__exit__(exc_type, exc_val, exc_tb)

    @property
    def command(self):
        return self.file.name


class SshRsh:
    def __init__(self, ansible_user, ansible_port):
        self.command = "ssh -o BatchMode=yes -p %s -l %s" % (
            shlex.quote(str(ansible_port)),
            shlex.quote(ansible_user),
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return


def sync_one_project_git(args, project, output):
    cwd = "%s/%s" % (args['executor_work_root'], project['src_dir'])
    dest = "%s/%s" % (args['zuul_workspace_root'], project['src_dir'])
    output['src'] = cwd
    output['dest'] = dest
    env = os.environ.copy()
    env['GIT_ALLOW_PROTOCOL'] = 'ext:ssh'
    # We occasionally see git pushes in the middle of this loop fail then
    # subsequent pushes for other repos succeed. The entire loop ends up
    # failing because one of the pushes failed. Mitigate this by retrying
    # on failure.
    max_tries = 3
    start = time.monotonic()
    for count in range(max_tries):
        try:
            if args['ansible_connection'] == "kubectl":
                git_dest = get_k8s_dest(args, dest)
            else:
                git_dest = get_ssh_dest(args, dest)
            out = run("git push --quiet --mirror %s" % (git_dest,),
                      cwd=cwd, env=env)
            output['push'] = out.stdout.decode('utf8').strip()
            break
        except Exception:
            if count + 1 >= max_tries:
                raise
    end = time.monotonic()
    output['attempts'] = count + 1
    output['elapsed'] = end - start


def sync_one_project_rsync(args, project, output):
    src = "%s/%s/" % (args['executor_work_root'], project['src_dir'])
    dest = "%s/%s/" % (args['zuul_workspace_root'], project['src_dir'])
    output['src'] = src
    output['dest'] = dest
    rsync_dest = get_rsync_dest(args, dest)
    if args['ansible_connection'] == "kubectl":
        resource = args['zuul_resources'][args['inventory_hostname']]
        rsh_manager = KubectlRsh(resource)
    else:
        rsh_manager = SshRsh(args['ansible_user'], args['ansible_port'])
    with rsh_manager as rsh:
        command = ["rsync", "--quiet", "--no-progress",
                   "--blocking-io", "--archive", "--no-owner",
                   "--no-group", "--omit-dir-times", "--numeric-ids",
                   "-e", rsh.command, src, rsync_dest]
        output['rsync_command'] = command
        max_tries = 3
        start = time.monotonic()
        for count in range(max_tries):
            try:
                out = run(command)
                break
            except Exception:
                if count + 1 >= max_tries:
                    raise
    output['rsync'] = out.stdout.decode('utf8').strip()
    end = time.monotonic()
    output['attempts'] = count + 1
    output['elapsed'] = end - start


def sync_one_project(args, project, output):
    project_name = project['canonical_name']
    state = args['repo_prep_output'][project_name]['initial_state']
    if state == 'not-present':
        return sync_one_project_rsync(args, project, output)
    return sync_one_project_git(args, project, output)


def ansible_main():
    module = AnsibleModule(
        argument_spec=dict(
            ansible_connection=dict(type='str'),
            ansible_host=dict(type='str'),
            ansible_port=dict(type='int'),
            ansible_user=dict(type='str'),
            executor_work_root=dict(type='path'),
            inventory_hostname=dict(type='str'),
            mirror_workspace_quiet=dict(type='bool'),
            zuul_projects=dict(type='dict'),
            zuul_resources=dict(type='dict'),
            zuul_workspace_root=dict(type='path'),
            repo_prep_output=dict(type='dict'),
        )
    )

    output = {}
    if for_each_project(sync_one_project, module.params, output):
        module.exit_json(changed=True, output=output)
    else:
        module.fail_json("Failure synchronizing repos", output=output)


if __name__ == '__main__':
    ansible_main()
