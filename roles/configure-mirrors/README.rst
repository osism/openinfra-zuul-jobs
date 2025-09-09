An ansible role to configure services to use mirrors.

**Role Variables**

.. zuul:rolevar:: mirror_fqdn
   :default: {{ zuul_site_mirror_fqdn }}

   The base host for mirror servers.

.. zuul:rolevar:: mirror_use_ssl
   :default: False

   Use ssl to communicate to mirror endpoints. Note if the platform
   cannot use ssl (for example Ubuntu Xenial apt needs additional packages)
   this will still use http instead of https when set for that platform.

.. zuul:rolevar:: pypi_fqdn
   :default: {{ mirror_fqdn }}

   The base host for PyPi mirror server.

.. zuul:rolevar:: pypi_mirror

   URL to override the generated pypi mirror url based on
   :zuul:rolevar:`configure-mirrors.pypi_fqdn`.

.. zuul:rolevar:: set_apt_mirrors_trusted
   :default: False

   Set to True in order to tag APT mirrors as trusted, needed
   when accessing unsigned mirrors with newer releases like
   Ubuntu Bionic.

.. zuul:rolevar:: enable_deb_src_repos
   :default: False

   Set this to True in order to enable deb-src entries in sources.list
   configs for apt. Note this option currently only works on Debian
   (not Ubuntu) installations.

.. zuul:rolevar:: configure_mirrors_extra_repos
   :default: False

   Set to True to opt-in to installing extra repositories such
   as PowerTools and HighAvailability on centos-8-stream and
   backports for Debian/Ubuntu. The intent is to match the upstream
   distro state when this variable is set to False. Note that this
   role is not necessarily consistent with the repos that are
   enabled by default between distribution versions (centos stream
   8 vs. 9 for example).

.. zuul:rolevar:: configure_mirrors_components_9_stream
   :default: See `vars/CentOS-9.yaml`

   A list of the components that should be redirected to the
   `mirror_fqdn` when setting up a CentOS 9-stream host.  For example,
   your mirror may only mirror some components, or not the
   debug/source components, etc.
