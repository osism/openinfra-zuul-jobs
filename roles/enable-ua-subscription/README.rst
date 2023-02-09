Enable UA Subscription on a node.

For Ubuntu nodes, this role activates an Ubuntu advantage
subscription using a passed in token (ubuntu_ua_token.token).

**Role Variables**

.. zuul:rolevar:: ubuntu_ua_token
   :type: dict
   :default: None

   Dict used to specify Ubuntu advantage subscription information.
   ubuntu_ua_token.token is a subscription key.
