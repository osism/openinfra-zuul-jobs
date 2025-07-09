# Copyright 2014 Rackspace Australia
# Copyright 2018 Red Hat, Inc
# Copyright 2024 Acme Gating, LLC
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

import argparse
import concurrent.futures
import datetime
import logging
import os
import sys
import traceback

import openstack
import requests.exceptions
import keystoneauth1.exceptions

from ansible.module_utils.basic import AnsibleModule

SEGMENT_SIZE = 500000000  # 500MB


def get_cloud(cloud):
    if isinstance(cloud, dict):
        config = openstack.config.loader.OpenStackConfig().get_one(**cloud)
        return openstack.connection.Connection(
            config=config,
            pool_executor=concurrent.futures.ThreadPoolExecutor(
                max_workers=10
            ))
    else:
        return openstack.connect(cloud=cloud)


def _add_etag_to_manifest(self, *args, **kw):
    return


def prune(cloud, container, delete_after):
    # In case the automatic expiration doesn't work, manually prune old uploads
    if not delete_after:
        return
    target = (datetime.datetime.now(datetime.UTC) -
              datetime.timedelta(seconds=delete_after))
    endpoint = cloud.object_store.get_endpoint()
    url = os.path.join(endpoint, container)
    for obj in cloud.object_store.objects(container):
        ts = datetime.datetime.fromisoformat(obj['last_modified'])
        ts = ts.replace(tzinfo=datetime.UTC)
        if ts < target:
            path = os.path.join(url, obj.name)
            try:
                cloud.session.delete(path)
            except keystoneauth1.exceptions.http.NotFound:
                pass


def run(cloud, container, filename, name, delete_after=None):
    # Monkey-patch sdk so that the SLO upload does not add the etag;
    # this works around an issue with rackspace-flex.
    cloud.object_store._add_etag_to_manifest = _add_etag_to_manifest
    prune(cloud, container, delete_after)
    headers = {}
    if delete_after:
        headers['X-Delete-After'] = str(delete_after)
    endpoint = cloud.object_store.get_endpoint()
    cloud.object_store.create_object(
        container,
        name=name,
        filename=filename,
        segment_size=SEGMENT_SIZE,
        **headers)
    url = os.path.join(endpoint, container, name)
    return url


def ansible_main():
    module = AnsibleModule(
        argument_spec=dict(
            cloud=dict(required=True, type='raw', no_log=True),
            container=dict(required=True, type='str'),
            filename=dict(required=True, type='path'),
            name=dict(required=True, type='str'),
            delete_after=dict(type='int'),
        )
    )

    p = module.params
    cloud = get_cloud(p.get('cloud'))
    try:
        url = run(
            cloud,
            p.get('container'),
            p.get('filename'),
            p.get('name'),
            delete_after=p.get('delete_after'),
        )
    except (keystoneauth1.exceptions.http.HttpError,
            requests.exceptions.RequestException):
        s = "Error uploading to %s.%s" % (cloud.name, cloud.config.region_name)
        s += "\n" + traceback.format_exc()
        module.fail_json(
            changed=False,
            msg=s,
            cloud=cloud.name,
            region_name=cloud.config.region_name)
    module.exit_json(
        changed=True,
        url=url,
    )


def cli_main():
    parser = argparse.ArgumentParser(
        description="Upload image to swift"
    )
    parser.add_argument('--verbose', action='store_true',
                        help='show debug information')
    parser.add_argument('cloud',
                        help='Name of the cloud to use when uploading')
    parser.add_argument('container',
                        help='Name of the container to use when uploading')
    parser.add_argument('filename',
                        help='the file to upload')
    parser.add_argument('name',
                        help='the object name')
    parser.add_argument('--delete-after',
                        help='Number of seconds to delete object after '
                             'upload. Default is 3 days (259200 seconds) '
                             'and if set to 0 X-Delete-After will not be set',
                        type=int)

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        # Set requests log level accordingly
        logging.getLogger("requests").setLevel(logging.DEBUG)
        logging.getLogger("keystoneauth").setLevel(logging.INFO)
        logging.getLogger("stevedore").setLevel(logging.INFO)
        logging.captureWarnings(True)

    url = run(
        get_cloud(args.cloud),
        args.container,
        args.filename,
        args.name,
        delete_after=args.delete_after,
    )
    print(url)


if __name__ == '__main__':
    if not sys.stdin.isatty():
        ansible_main()
    else:
        cli_main()
