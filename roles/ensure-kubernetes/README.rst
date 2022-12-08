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

   Which kubernetes runtime to use for minikube; values are ``docker`` or
   ``cri-o``.

.. zuul:rolevar:: ensure_kubernetes_minikube_addons
   :default: []

   List of addons to configure in k8s. Use this to enable the addons.
