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

import time

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


def update_one_project(args, project, output):
    project_name = project['canonical_name']
    state = args['repo_prep_output'][project_name]['initial_state']

    cwd = "%s/%s" % (args['zuul_workspace_root'], project['src_dir'])
    output['dest'] = cwd

    start = time.monotonic()
    # Reset is needed because we pushed to a non-bare repo
    run("git reset --hard", cwd=cwd)
    # Clean is needed because we pushed to a non-bare repo
    run("git clean -xdf", cwd=cwd)
    if state != 'not-present':
        # Undo the config setting we did in repo_prep
        run("git config --local --unset receive.denyCurrentBranch", cwd=cwd)
        run("git config --local --unset receive.denyDeleteCurrent", cwd=cwd)
    # checkout the branch matching the branch set up by the executor
    out = run("git checkout --quiet %s" % (project['checkout'],), cwd=cwd)
    output['checkout'] = out.stdout.decode('utf8').strip()
    # put out a status line with the current HEAD
    out = run("git log --pretty=oneline -1", cwd=cwd)
    end = time.monotonic()
    output['HEAD'] = out.stdout.decode('utf8').strip()
    output['elapsed'] = end - start


def ansible_main():
    module = AnsibleModule(
        argument_spec=dict(
            zuul_projects=dict(type='dict'),
            zuul_workspace_root=dict(type='path'),
            repo_prep_output=dict(type='dict'),
        )
    )

    output = {}
    if for_each_project(update_one_project, module.params, output):
        module.exit_json(changed=True, output=output)
    else:
        module.fail_json("Failure updating repos", output=output)


if __name__ == '__main__':
    ansible_main()
