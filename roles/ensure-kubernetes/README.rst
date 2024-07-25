An ansible role to install kubernetes.

**Role Variables**

.. zuul:rolevar:: ensure_kubernetes_type
   :default: minikube

   The kubernetes distribution to use.  Currently ```minikube`` or
   ```microk8s```.  Note that ```microk8s``` is only implemented for
   Ubuntu Jammy distributions currently.

.. zuul:rolevar:: ensure_kubernetes_microk8s_channel
   :default: latest/stable

   The ``snap`` channel to use for ```microk8s```.  See
   `<https://microk8s.io/docs/setting-snap-channel>`__.

.. zuul:rolevar:: ensure_kubernetes_microk8s_addons
   :default: ['dns', 'storage']

   The addons for ``microk8s```.  See
   `<https://microk8s.io/docs/addons>`__

.. zuul:rolevar:: install_kubernetes_with_cluster
   :default: True

   If true, installs a Minikube cluster.

.. zuul:rolevar:: minikube_version
   :default: latest

   The version of Minikube to install.

.. zuul:rolevar:: minikube_dns_resolvers
   :default: []

   List of dns resolvers to configure in k8s. Use this to override the
   resolvers that are found by default.

.. zuul:rolevar:: kubernetes_runtime
   :default: docker

   Which kubernetes runtime to use for minikube; values are ``docker``,
   ``cri-o`` or ``podman``. For any other values the
   ``ensure_kubernetes_minikube_*`` options will be used instead. Please
   note that only some combinations of profiles and distros might be
   valid.

.. zuul:rolevar:: ensure_kubernetes_minikube_addons
   :default: []

   List of addons to configure in k8s. Use this to enable the addons.

.. zuul:rolevar:: ensure_kubernetes_minikube_driver
   :default: none

   Which driver to use for minikube. The default is the ``none`` driver.
   See also ``kubernetes_runtime``.

.. zuul:rolevar:: ensure_kubernetes_minikube_runtime
   :default: docker

   Which kubernetes runtime to use for minikube. See also
   ``kubernetes_runtime``.

.. zuul:rolevar:: ensure_kubernetes_minikube_provider
   :default: docker

   Which container provider to use for minikube. See also
   ``kubernetes_runtime``.

.. zuul:rolevar:: ensure_kubernetes_bin_path
   :default: /tmp

   Where to install binaries for minikube. This is currently set to retain
   compatibility with existing users, but the intention is to move the
   install default to a more sane location in the future.

.. zuul:rolevar:: ensure_kubernetes_minikube_memory
   :default: no-limit

   For the ``podman`` runtime, the podman container running the entire
   minikube instance can have a global memory limit applied. The default
   value sets no limit.

.. zuul:rolevar:: ensure_kubernetes_minikube_cpus
   :default: no-limit

   For the ``podman`` runtime, the podman container running the entire
   minikube instance can have a global cpu limit applied. The default
   value sets no limit.
