Install skopeo

**Role Variables**

.. zuul:rolevar:: ensure_skopeo_install_from_upstream
   :default: false

   Build and install skopeo from upstream.  This installs a go
   development environment and build dependencies.  The binary is
   installed into ``/usr/local/bin``.

   Currently only implemented for Ubuntu Jammy.

.. zuul:rolevar:: ensure_skopeo_install_from_upstream_version
   :default: v1.9.3

   When building skopeo locally, the version tag to use.
