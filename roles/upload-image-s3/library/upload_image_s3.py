# Copyright 2014 Rackspace Australia
# Copyright 2018 Red Hat, Inc
# Copyright 2024-2025 Acme Gating, LLC
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
import base64
import datetime
import logging
import multiprocessing
import os
import sys
import traceback
import zlib

import boto3

from ansible.module_utils.basic import AnsibleModule


def calculate_crc32(queue, filename):
    ret = 0
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            ret = zlib.crc32(data, ret)
    queue.put(ret)


def prune(bucket, delete_after):
    # In case the automatic expiration doesn't work, manually prune old uploads
    if not delete_after:
        return
    target = (datetime.datetime.now(datetime.UTC) -
              datetime.timedelta(seconds=delete_after))
    for obj in bucket.objects.all():
        if obj.last_modified < target:
            obj.delete()


def run(endpoint, bucket_name, aws_access_key, aws_secret_key,
        filename, name, delete_after=None, export_s3_url=False):
    endpoint = endpoint or 'https://s3.amazonaws.com/'
    s3 = boto3.resource('s3',
                        endpoint_url=endpoint,
                        aws_access_key_id=aws_access_key,
                        aws_secret_access_key=aws_secret_key)
    s3_client = boto3.client('s3',
                             endpoint_url=endpoint,
                             aws_access_key_id=aws_access_key,
                             aws_secret_access_key=aws_secret_key)
    bucket = s3.Bucket(bucket_name)

    # Immediately start the background crc32 calculation
    queue = multiprocessing.Queue()
    crc32_proc = multiprocessing.Process(target=calculate_crc32,
                                         args=(queue, filename))
    crc32_proc.start()

    # Prune any lingering uploads
    prune(bucket, delete_after)

    # Start the upload
    bucket.upload_file(
        filename, name,
        ExtraArgs={
            'ChecksumType': 'FULL_OBJECT',
        },
    )

    resp = s3_client.head_object(
        Bucket=bucket_name,
        Key=name,
        ChecksumMode='ENABLED',
    )
    aws_checksum = resp.get('ChecksumCRC32')
    if aws_checksum:
        aws_checksum = base64.b64decode(aws_checksum).hex()
        crc32_proc.join()
        local_checksum = '%08x' % queue.get()
        if aws_checksum != local_checksum:
            raise Exception(f"AWS checksum {aws_checksum} does not match "
                            f"local checksum {local_checksum}")

    if export_s3_url:
        url = os.path.join("s3://", bucket_name, name)
    else:
        url = os.path.join(endpoint, bucket_name, name)
    return url, aws_checksum


def ansible_main():
    module = AnsibleModule(
        argument_spec=dict(
            endpoint=dict(type='str'),
            bucket=dict(required=True, type='str'),
            filename=dict(required=True, type='path'),
            name=dict(required=True, type='str'),
            delete_after=dict(type='int'),
            export_s3_url=dict(type='bool', default=False),
            aws_access_key=dict(type='str'),
            aws_secret_key=dict(type='str', no_log=True),
        )
    )

    p = module.params

    try:
        url, checksum = run(
            p.get('endpoint'),
            p.get('bucket'),
            p.get('aws_access_key'),
            p.get('aws_secret_key'),
            p.get('filename'),
            p.get('name'),
            delete_after=p.get('delete_after'),
            export_s3_url=p.get('export_s3_url'),
        )
    except Exception:
        s = "Error uploading to S3"
        s += "\n" + traceback.format_exc()
        module.fail_json(
            changed=False,
            msg=s)
    module.exit_json(
        changed=True,
        url=url,
        checksum=checksum,
    )


def cli_main():
    parser = argparse.ArgumentParser(
        description="Upload image to S3"
    )
    parser.add_argument('--verbose', action='store_true',
                        help='show debug information')
    parser.add_argument('--endpoint',
                        help='http endpoint of s3 service')
    parser.add_argument('bucket',
                        help='Name of the bucket to use when uploading')
    parser.add_argument('filename',
                        help='the file to upload')
    parser.add_argument('name',
                        help='the object name')
    parser.add_argument('--delete-after',
                        help='Number of seconds to delete object after '
                             'upload. Default is 3 days (259200 seconds) '
                             'and if set to 0 X-Delete-After will not be set',
                        type=int)
    parser.add_argument('--export-s3-url',
                        help='Export the image location as s3:// URL',
                        action='store_true')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.captureWarnings(True)

    url, checksum = run(
        args.endpoint,
        args.bucket,
        None,
        None,
        args.filename,
        args.name,
        delete_after=args.delete_after,
        export_s3_url=args.export_s3_url,
    )
    print(checksum)
    print(url)


if __name__ == '__main__':
    if not sys.stdin.isatty():
        ansible_main()
    else:
        cli_main()
