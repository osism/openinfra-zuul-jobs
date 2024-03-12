#!/usr/bin/env python
#
# Copyright 2019 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# Update job definitions for multi-platform jobs, and make sure every
# in-repo test job appears in a project definition.  This script
# re-writes the files in zuul-tests.d.  It should be run from the root
# of the repo.

import os
import sys

from ruamel.yaml.comments import CommentedMap

import ruamellib

# There are fedora- and debian-latest nodesets, but they can't be used
# in the multinode jobs, so just use the real labels everywhere.

CENTOS_PLATFORMS = [
    'centos-8-stream',
    'centos-9-stream',
]
DEBIAN_PLATFORMS = [
    'debian-bullseye',
    'debian-bookworm',
]
UBUNTU_PLATFORMS = [
    'ubuntu-bionic',
    'ubuntu-focal',
    'ubuntu-jammy',
]
FEDORA_PLATFORMS = [
]
OTHER_PLATFORMS = [
    # 'gentoo-17-0-systemd',
]
ALL_PLATFORMS = (CENTOS_PLATFORMS + DEBIAN_PLATFORMS +
                 UBUNTU_PLATFORMS + FEDORA_PLATFORMS +
                 OTHER_PLATFORMS)

# insert a platform from above to make it non-voting
NON_VOTING = [
]

TAGS = {
    'centos-platforms': CENTOS_PLATFORMS,
    'debian-platforms': DEBIAN_PLATFORMS,
    'ubuntu-platforms': UBUNTU_PLATFORMS,
    'debuntu-platforms': UBUNTU_PLATFORMS + DEBIAN_PLATFORMS,
    'fedora-platforms': FEDORA_PLATFORMS,
    'all-platforms': ALL_PLATFORMS,
}

# Insert a job to make that single job non-voting
NON_VOTING_JOBS = [
    'zuul-jobs-test-multinode-roles-gentoo-17-0-systemd',
]


def get_nodeset(platform, multinode):
    d = CommentedMap()
    if not multinode:
        d['nodes'] = [
            CommentedMap([('name', platform), ('label', platform)]),
        ]
    else:
        d['nodes'] = [
            CommentedMap([('name', 'primary'), ('label', platform)]),
            CommentedMap([('name', 'secondary'), ('label', platform)]),
        ]
        d['groups'] = [
            CommentedMap([('name', 'switch'), ('nodes', ['primary'])]),
            CommentedMap([('name', 'peers'), ('nodes', ['secondary'])]),
        ]
    return d


def handle_file(fn):
    yaml = ruamellib.YAML()
    data = yaml.load(open(fn))
    outdata = []
    outprojects = []
    joblist_check = []
    joblist_gate = []
    has_non_voting = False
    for obj in data:
        if 'job' in obj:
            job = obj['job']
            if 'auto-generated' in job.get('tags', []):
                continue
            outdata.append(obj)
            tags = job.get('tags', [])
            platforms = set()
            multinode = 'multinode' in tags
            for key, data in TAGS.items():
                if key in tags:
                    platforms.update(data)
            platforms = sorted(platforms)
            if platforms:
                for platform in platforms:
                    voting = False if platform in NON_VOTING else True
                    ojob = CommentedMap()
                    ojob['name'] = job['name'] + '-' + platform
                    if ojob['name'] in NON_VOTING_JOBS:
                        voting = False
                    if not voting:
                        ojob['name'] += '-nv'
                        ojob['voting'] = False
                        has_non_voting = True
                    desc = job['description'].split('\n')[0]
                    ojob['description'] = desc + ' on ' \
                        + platform
                    ojob['parent'] = job['name']
                    ojob['tags'] = 'auto-generated'
                    ojob['nodeset'] = get_nodeset(platform, multinode)
                    outdata.append({'job': ojob})
                    joblist_check.append(ojob['name'])
                    if voting:
                        joblist_gate.append(ojob['name'])
            elif not job.get('abstract', False):
                joblist_check.append(job['name'])
                # don't append non-voting jobs to gate
                if job.get('voting', True):
                    joblist_gate.append(job['name'])
                else:
                    has_non_voting = True
        elif 'project' in obj:
            outprojects.append(obj)
        else:
            outdata.append(obj)
    # We control the last project stanza
    outdata.extend(outprojects)
    if not outprojects:
        seed = """
- project:
    check:
      jobs: []
    gate:
      jobs: []
"""
        print(
            f"FATAL: File {fn} last item is not a project definition. "
            f"Try adding something like:\n{seed}")
        sys.exit(1)
    project = outprojects[-1]['project']
    project['check']['jobs'] = joblist_check
    # Use the same dictionary if there are no non-voting jobs
    # (i.e. check is the same as gate); this gives nicer YAML output
    # using dictionary anchors
    project['gate']['jobs'] = joblist_gate if has_non_voting else joblist_check
    # gate jobs should also be in periodic in order to assure they do not rot
    periodic_pipeline = 'periodic-weekly'
    if periodic_pipeline not in project:
        project[periodic_pipeline] = {}
    if 'jobs' not in project[periodic_pipeline]:
        project[periodic_pipeline]['jobs'] = []
    project[periodic_pipeline]['jobs'] = joblist_gate \
        if has_non_voting else joblist_check

    with open(fn, 'w') as f:
        yaml.dump(outdata, stream=f)


def main():
    for f in os.listdir('zuul-tests.d'):
        if not f.endswith('.yaml'):
            continue
        if f == 'project.yaml':
            continue
        handle_file(os.path.join('zuul-tests.d', f))


if __name__ == "__main__":
    main()
