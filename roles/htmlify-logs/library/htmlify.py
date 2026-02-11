# Copyright 2018 Red Hat, Inc
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

try:
    import html
    html_escape = html.escape
except ImportError:
    import cgi
    html_escape = cgi.escape

import argparse
import gzip
import sys

from ansible.module_utils.basic import AnsibleModule

HEADER = '''<html>
<head>
<style>
a {color: #000; text-decoration: none}
a:hover {text-decoration: underline}
#selector, #selector a {color: #888}
#selector a:hover {color: #c00}
.highlight {
    background-color: rgb(255, 255, 204);
}
</style>
</head>
<body>
<pre>
'''

FOOTER = '''</pre>
</body>
<script>
var old_highlight;

function remove_highlight() {
    if (old_highlight) {
        items = document.getElementsByClassName(old_highlight);
        for (var i = 0; i < items.length; i++) {
            items[i].className = items[i].className.replace('highlight','');
        }
    }
}

function update_selector(highlight) {
    var selector = document.getElementById('selector');
    if (selector) {
        var links = selector.getElementsByTagName('a');
        for (var i = 0; i < links.length; i++) {
            links[i].hash = "#" + highlight;
        }
    }
}

function highlight_by_hash(event) {
    var highlight = window.location.hash.substr(1);
    // handle changes to highlighting separate from reload
    if (event) {
         highlight = event.target.hash.substr(1);
    }
    remove_highlight();
    if (highlight) {
        elements = document.getElementsByClassName(highlight);
        for (var i = 0; i < elements.length; i++) {
            elements[i].className += " highlight";
        }
        update_selector(highlight);
        old_highlight = highlight;
    }
}
document.onclick = highlight_by_hash;
highlight_by_hash();
</script>
</html>
'''


def run(inpath, outpath):
    if inpath.endswith('.gz'):
        infile = gzip.open(inpath, 'rt')
        outfile = gzip.open(outpath, 'wt')
    else:
        infile = open(inpath, 'r')
        outfile = open(outpath, 'w')

    outfile.write(HEADER)

    for i, line in enumerate(infile):
        i = i + 1
        line = html_escape(line.rstrip('\n'))
        outfile.write('<a name="l%s" class="l%s" href="#l%s">' % (i, i, i))
        outfile.write(line.rstrip('\n'))
        outfile.write("</a>\n")

    outfile.write(FOOTER)


def ansible_main():
    module = AnsibleModule(
        argument_spec=dict(
            input=dict(required=True, type='path'),
            output=dict(required=True, type='path'),
        )
    )

    p = module.params
    run(p.get('input'), p.get('output'))

    module.exit_json(changed=True)


def cli_main():
    parser = argparse.ArgumentParser(
        description="HTMLify text files"
    )
    parser.add_argument('input',
                        help='Input path')
    parser.add_argument('output',
                        help='Output path')

    args = parser.parse_args()

    run(args.input, args.output)


if __name__ == '__main__':
    # The zip/ansible/modules check is required for Ansible 5 because
    # stdin may be a tty, but does not work in ansible 2.8.  The tty
    # check works on versions 2.8, 2.9, and 6.
    if ('.zip/ansible/modules' in sys.argv[0] or not sys.stdin.isatty()):
        ansible_main()
    else:
        cli_main()
