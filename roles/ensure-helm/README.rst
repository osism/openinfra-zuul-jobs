Ensure Helm is installed

Currently, this role always downloads and installs the requested version
of helm.

**Role Variables**

.. zuul:rolevar:: helm_version
   :default: 2.17.0

   Version of Helm to install. For historical reasons this does not include
   the "v" prefix. Use "latest" to probe for the latest release.

.. zuul:rolevar:: helm_release_repo_url
   :default: https://get.helm.sh

   The repo where the helm releases should be fetched from.

.. zuul:rolevar:: helm_install_dir
   :default: /usr/local/bin

   The installation directory for helm.
