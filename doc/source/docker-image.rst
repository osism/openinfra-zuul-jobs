Container Images
================

This repo has several jobs which can form the basis of a system
supporting a full gating process for continuously deployed container
images.  They can be used to build or test images which rely on other
images using the full power of Zuul's speculative execution.

In order to use these jobs to their full potential, the Zuul site
administrator will need to run a simple but dedicated container image
registry, and define local versions of the jobs to use it.  The
following sections describe how to define those jobs and how the
system is intended to work once the jobs are defined.

.. contents::
   :local:

Run an Intermediate Container Registry
--------------------------------------

A dedicated container registry is required for the use of these jobs.
It is merely used to temporarily hold images so that they can be
transferred between jobs running in different projects at different
times.  It does not need to be publicly accessible or particularly
robust.  If its backing storage fails and needs to be replaced, the
only result is that some jobs running in Zuul may fail and may need to
be re-run.  In this system, it is called the "intermediate registry"
to distinguish it from other registry services.

You may run the registry in whatever manner is appropriate for your
site.  The following docker-compose file may be used as an example
of a working deployment suitable for production:

.. code-block:: yaml

   services:
     registry:
       restart: always
       image: registry:2
       network_mode: host
       environment:
         REGISTRY_HTTP_TLS_CERTIFICATE: /certs/domain.crt
         REGISTRY_HTTP_TLS_KEY: /certs/domain.key
         REGISTRY_AUTH: htpasswd
         REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
         REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
       volumes:
         - /var/registry/data:/var/lib/registry
         - /var/registry/certs:/certs
         - /var/registry/auth:/auth

You will need to provide the SSL certificate and key values, as well
as the htpassword file with a user and password already present.

Once that service is running, create the following four jobs in a
Zuul config-project:

Create Parent Jobs
------------------

.. _yoursite-buildset-registry:

yoursite-buildset-registry
~~~~~~~~~~~~~~~~~~~~~~~~~~

This job is used to provide a temporary "buildset registry" to jobs
running in your system; it communicates with the "intermediate"
registry described above.

.. code-block:: yaml
   :caption: zuul.yaml

   - secret:
       name: yoursite-intermediate-registry
       data:
         host: insecure-ci-registry.example.org
         port: 5000
         username: zuul
         password: !encrypted/pkcs1-oaep
           - ...

   - job:
       name: yoursite-buildset-registry
       pre-run: playbooks/buildset-registry/pre.yaml
       run: playbooks/buildset-registry/run.yaml
       post-run: playbooks/buildset-registry/post.yaml
       secrets:
         - secret: yoursite-intermediate-registry
           name: intermediate_registry
       requires: docker-image

The credentials in the secret should match those you supplied when
creating the intermediate registry.

The ``requires: docker-image`` attribute means that whenever this job
(or any jobs which inherit from it) run, Zuul will search ahead of the
change in the dependency graph to find any jobs which produce
docker-images and tell this job about them.  This allows the job to
pull images from the intermediate registry into the buildset registry.

.. code-block:: yaml
   :caption: playbooks/buildset-registry/pre.yaml

   - hosts: all
     tasks:
       - name: Install docker
         include_role:
           name: ensure-docker
       - name: Run buildset registry (if not already running)
         when: buildset_registry is not defined
         include_role:
           name: run-buildset-registry
       - name: Use buildset registry
         include_role:
           name: use-buildset-registry

   - hosts: localhost
     roles:
       - pull-from-intermediate-registry

This playbook runs a buildset registry if one isn't already running.
It returns the connection information back to Zuul in a variable
called ``buildset_registry``.  Other jobs will use that to learn how
to connect to the registry, and we can use that here to find out if
one was already started in a previous job.  We will use that facility
in the :ref:`yoursite-build-docker-image` job below.

.. code-block:: yaml
   :caption: playbooks/buildset-registry/run.yaml

   - hosts: localhost
     tasks:
       - name: Pause the job
         zuul_return:
           data:
             zuul:
               pause: true

The ``pause`` causes the job to wait until all jobs which depend on
this one are completed.

.. code-block:: yaml
   :caption: playbooks/buildset-registry/post.yaml

   - hosts: localhost
     roles:
       - push-to-intermediate-registry

.. _yoursite-build-docker-image:

yoursite-build-docker-image
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This job builds one or more docker images and interacts with the
buildset and intermediate registries.

.. code-block:: yaml
   :caption: zuul.yaml

   - job:
       name: yoursite-build-docker-image
       parent: yoursite-buildset-registry
       run: playbooks/docker-image/run.yaml
       provides: docker-image

Note that the parent of this job is :ref:`yoursite-buildset-registry`.
This means that a simple repo that only needs to support one image
building job and doesn't have any other jobs which require a buildset
registry can just add this job alone and it will run a buildset
registry on the build host.  More complex scenarios would run the
:ref:`yoursite-buildset-registry` job on its own and construct a job
graph that depends on it.  Because the pre-run playbook in the
buildset-registry job only runs a buildset registry if one isn't
already running, it can be used for both cases.  And because the run
playbook which pauses the job is overridden in this job, this job will
not pause.

.. code-block:: yaml
   :caption: playbooks/docker-image/run.yaml

   - hosts: all
     roles:
       - build-docker-image

.. _yoursite-upload-docker-image:

yoursite-upload-docker-image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This job further builds on the :ref:`yoursite-build-docker-image` job
and additionally uploads the image to Docker Hub.  Depending on the
situation, you could encode the Docker Hub credentials into this job
as a secret, or you could allow other users to provide them via the
`pass-to-parent <https://zuul-ci.org/docs/zuul/user/config.html#attr-job.secrets.pass-to-parent>`_ feature of secrets.

.. code-block:: yaml
   :caption: zuul.yaml

   - job:
       name: yoursite-upload-docker-image
       parent: yoursite-build-docker-image
       post-run: playbooks/docker-image/upload.yaml

.. code-block:: yaml
   :caption: playbooks/docker-image/upload.yaml

   - hosts: all
     roles:
       - upload-docker-image

.. _yoursite-promote-docker-image:

yoursite-promote-docker-image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This job does nothing that the :zuul:job:`promote-docker-image` job in
this repo doesn't already do, but since you created local versions of
the other two jobs, you should make one of this as well for
consistency.  If you chose to add Docker Hub credentials to the
:ref:`yoursite-upload-docker-image` job, you should do that here as
well.

.. code-block:: yaml
   :caption: zuul.yaml

   - job:
       name: yoursite-promote-docker-image
       parent: promote-docker-image

System Architecture
-------------------

Now that those jobs are defined, this section describes how they work
together.

There are a few key concepts to keep in mind:

A *buildset* is a group of jobs all running on the same change.

A *buildset registry* is a container image registry which is used to
store speculatively built images for the use of jobs in a single
buildset.  It holds the differences between the current state of the
world and the future state if the change in question (and all of its
dependent changes) were to merge.  It must be started by one of the
jobs in a buildset, and it ceases to exist once that job is complete.

An *intermediate registry* is a long-running registry that is used to
store images created for unmerged changes for use by other unmerged
changes.  It is not publicly accessible and is intended only to be
used by Zuul in order to transfer artifacts from one buildset to
another.

With these concepts in mind, the jobs described above implement the
following workflow for a single change:

..
   The below diagram was adapted from the TCP flow example here
   https://stackoverflow.com/questions/32436856/using-graphviz-to-create-tcp-flow-diagrams

.. _buildset_image_transfer:

.. graphviz::
   :caption: Buildset registry image transfer

   digraph image_transfer {
     splines=false
     nodesep=1

     // Set things up like a spreadsheet grid as I found that simplifies
     // remembering which nodes have edges between them.
     ir_start [label="Intermediate\nRegistry" shape="box"]
     ir_end [style=invis]
     ir_0 [label="" shape=point height=.005]
     ir_1 [label="" shape=point height=.005]
     ir_2 [label="" shape=point height=.005]
     ir_3 [label="" shape=point height=.005]
     ir_4 [label="" shape=point height=.005]
     ir_5 [label="" shape=point height=.005]
     ir_start -> ir_0 -> ir_1 -> ir_2 -> ir_3 -> ir_4 -> ir_5 -> ir_end [arrowhead="none" style="bold"]

     br_start [label="Buildset\nRegistry" shape="box"]
     br_end [style=invis]
     br_0 [label="" shape=point height=.005]
     br_1 [label="" shape=point height=.005]
     br_2 [label="" shape=point height=.005]
     br_3 [label="" shape=point height=.005]
     br_4 [label="" shape=point height=.005]
     br_5 [label="" shape=point height=.005]
     br_start -> br_0 -> br_1 -> br_2 -> br_3 -> br_4 -> br_5 [arrowhead="none" style="bold"]
     br_5 -> br_end [arrowhead="none" style="dashed"]

     ij_start [label="Image\nBuild Job" shape="box"]
     ij_end [style=invis]
     ij_0 [label="" shape=point height=.005]
     ij_1 [label="" shape=point height=.005]
     ij_2 [label="" shape=point height=.005]
     ij_3 [label="" shape=point height=.005]
     ij_4 [label="" shape=point height=.005]
     ij_5 [label="" shape=point height=.005]
     ij_start -> ij_0 -> ij_1 [arrowhead="none" style="dashed"]
     ij_1 -> ij_2 [arrowhead="none" style="bold"]
     ij_2 -> ij_3 -> ij_4 -> ij_5 -> ij_end [arrowhead="none" style="dashed"]

     tj_start [label="Deployment\nTest Job" shape="box"]
     tj_end [style=invis]
     tj_0 [label="" shape=point height=.005]
     tj_1 [label="" shape=point height=.005]
     tj_2 [label="" shape=point height=.005]
     tj_3 [label="" shape=point height=.005]
     tj_4 [label="" shape=point height=.005]
     tj_5 [label="" shape=point height=.005]
     tj_start -> tj_0 -> tj_1 -> tj_2 -> tj_3 -> tj_4 [arrowhead="none" style="dashed"]
     tj_4 -> tj_5 [arrowhead="none" style="bold"]
     tj_5 -> tj_end [arrowhead="none" style="dashed"]

     {rank=same;ir_start;br_start;ij_start;tj_start}
     {rank=same;ir_0;br_0;ij_0;tj_0}
     {rank=same;ir_1;br_1;ij_1;tj_1}
     {rank=same;ir_2;br_2;ij_2;tj_2}
     {rank=same;ir_3;br_3;ij_3;tj_3}
     {rank=same;ir_4;br_4;ij_4;tj_4}
     {rank=same;ir_5;br_5;ij_5;tj_5}
     {rank=same;ir_end;br_end;ij_end;tj_end}

     // Flows between first and second column
     ir_0 -> br_0 [weight=0 label="Images from previous changes"]
     br_3 -> ir_3 [weight=0 label="Current image"]
     ir_end -> br_end [weight=0 style=invis]

     // Flows between second and third column
     br_1 -> ij_1 [weight=0 label="Images from previous changes"]
     ij_2 -> br_2 [weight=0 label="Current image"]
     br_end -> ij_end [weight=0 style=invis]

     // Flows between second and fourth column
     br_4 -> tj_4 [weight=0 xlabel="Current and previous images" ]
   }

The intermediate registry is always running and the buildset registry
is started by a job running on a change.  The "Image Build" and
"Deployment Test" jobs are example jobs which might be running on a
change.  Essentially, these are image producer or consumer jobs
respectively.

Using the Jobs
--------------

There are two ways to use the jobs described above:

A Repository with Producers and Consumers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first is in a repository where images are both produced and
consumed.  In this case, we can expect that there will be at least one
image build job, and at least one job which uses that image (for
example, by performing a test deployment of the image).  In this case
we need to construct a job graph with dependencies as follows:

.. graphviz::

   digraph dependencies {
     rankdir="LR";
     node [shape=box];
     "yoursite-\nbuildset-registry" -> "build-image" [dir=back];
     "build-image" -> "test-image" [dir=back];
   }

The :ref:`yoursite-buildset-registry` job will run first and
automatically start a buildset registry populated with images built
from any changes which appear ahead of the current change.  It will
then return its connection information to Zuul and pause and continue
running until the completion of the build and test jobs.

The build-image job should inherit from
:ref:`yoursite-build-docker-image`, which will ensure that it is
automatically configured to use the buildset registry.

The test-image job is something that you will create yourself.  There
is no standard way to test or deploy an image, that depends on your
application.  However, there is one thing you will need to do in your
job to take advantage of the buildset registry.  In a pre-run playbook,
use the `use-buildset-registry
<https://zuul-ci.org/docs/zuul-jobs/roles.html#role-use-buildset-registry>`_
role:

.. code-block:: yaml

   - hosts: all
     roles:
       - use-buildset-registry

That will configure the docker daemon on the host to use the buildset
registry so that it will use the newly built version of any required
images.

A Repository with Only Producers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The second way to use these jobs is in a repository where an image is
merely built, but not deployed.  In this case, there are no consumers
of the buildset registry other than the image build job, and so the
registry can be run on the job itself.  In this case, you may omit the
:ref:`yoursite-buildset-registry` job and run only the
:ref:`yoursite-build-docker-image` job.

Publishing an Image
~~~~~~~~~~~~~~~~~~~

So far we've covered the image building process.  This system also
provides two more jobs that are used in publishing images to Docker
Hub.

The :ref:`yoursite-upload-docker-image` job does everything the
:ref:`yoursite-build-docker-image` job does, but it also uploads
the built image to Docker Hub using an automatically-generated and
temporary tag.  The "build" job is designed to be used in the
*check* pipeline, while the "upload" job is designed to take its
place in the *gate* pipeline.  By front-loading the upload to Docker
Hub, we reduce the chance that a credential or network error will
prevent us from publishing an image after a change lands.

The :ref:`yoursite-promote-docker-image` job is designed to be
used in the *promote* pipeline and simply re-tags the image on Docker
Hub after the change lands.

Keeping in mind that everything described above in
:ref:`buildset_image_transfer` applies to the
:ref:`yoursite-upload-docker-image` job, the following illustrates
the additional tasks performed by the "upload" and "promote" jobs:

..
   The below diagram was adapted from the TCP flow example here
   https://stackoverflow.com/questions/32436856/using-graphviz-to-create-tcp-flow-diagrams

.. graphviz::

   digraph image_transfer {
     splines=false
     nodesep=1

     // Set things up like a spreadsheet grid as I found that simplifies
     // remembering which nodes have edges between them.
     dh_start [label="Docker Hub" shape="box"]
     dh_end [style=invis]
     dh_0 [label="" shape=point height=.005]
     dh_1 [label="" shape=point height=.005]
     dh_2 [label="" shape=point height=.005]
     dh_start -> dh_0 -> dh_1 -> dh_2 -> dh_end [arrowhead="none" style="bold"]

     ui_start [label="upload-image" shape="box"]
     ui_end [style=invis]
     ui_0 [label="" shape=point height=.005]
     ui_1 [label="" shape=point height=.005]
     ui_2 [label="" shape=point height=.005]
     ui_start -> ui_0 [arrowhead="none" style="bold"]
     ui_0 -> ui_1 -> ui_2 -> ui_end [arrowhead="none" style="dashed"]

     pi_start [label="promote-image" shape="box"]
     pi_end [style=invis]
     pi_0 [label="" shape=point height=.005]
     pi_1 [label="" shape=point height=.005]
     pi_2 [label="" shape=point height=.005]
     pi_start -> pi_0 -> pi_1 [arrowhead="none" style="dashed"]
     pi_1 -> pi_2 [arrowhead="none" style="bold" xlabel="Only the manifest\nis transferred,\nnot the actual\nimage layers"]
     pi_2 -> pi_end [arrowhead="none" style="dashed"]


     {rank=same;dh_start;ui_start;pi_start}
     {rank=same;dh_0;ui_0;pi_0}
     {rank=same;dh_1;ui_1;pi_1}
     {rank=same;dh_2;ui_2;pi_2}
     {rank=same;dh_end;ui_end;pi_end}

     // Flows between first and second column
     ui_0 -> dh_0 [weight=0 label="Current Image with Temporary Tag"]
     dh_end -> ui_end [weight=0 style=invis]

     // Flows between first and third column
     dh_1 -> ui_1 [weight=0 arrowhead="none"]
     ui_1 -> pi_1 [weight=0 label="Current Image Manifest\nwith Temporary Tag"]
     pi_2 -> ui_2 [weight=0 label="Current Image Manifest\nwith Final Tag" arrowhead="none"]
     ui_2 -> dh_2 [weight=0]
     dh_end -> pi_end [weight=0 style=invis]
   }
