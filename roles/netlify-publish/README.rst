Publish built site to netlify

**Role Variables**

.. zuul:rolevar:: netlify_site_id

   Site id for the site to publish. This can be found on the site
   general settings page as ``API Id``.

.. zuul:rolevar:: netlify_auth

   Complex argument which contains the netlify authentication credentials.
   This is expected to come from a secret.

   .. zuul:rolevar:: token

      API token to use to publish the content. Instructions for creating
      a token can be found at
      https://docs.netlify.com/cli/get-started/#obtain-a-token-in-the-netlify-ui

.. zuul:rolevar:: zuul_work_dir
   :default: {{ zuul.project.src_dir }}

   The project directory.
