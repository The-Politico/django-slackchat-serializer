.. _config-options:

Configuration options
=====================


Required config
---------------

:code:`SLACKCHAT_SLACK_VERIFICATION_TOKEN`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Slack app `verification token <https://api.slack.com/docs/token-types#verification_tokens>`_.

:code:`SLACKCHAT_SLACK_API_TOKEN`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Slack app `OAuth access token <https://api.slack.com/docs/token-types#user>`_.

:code:`SLACKCHAT_PUBLISH_ROOT`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The URL root of your front end. It will be combined with the :code:`publish_path` of both the :code:`ChatType` and :code:`Channel` to create preview links in the CMS.

For example, if you have a :code:`ChatType` with the :code:`publish_path` of :code:`/my-custom-type/` and your channel's :code:`publish_path` is :code:`my-chat` you might expect that this chat will be published at :code:`https://my-site.com/slack-chats/my-custom-type/my-chat/`. In this case your :code:`SLACKCHAT_PUBLISH_ROOT` would be :code:`https://my-site.com/slack-chats/`.

:code:`SLACKCHAT_TEAM_ROOT`
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The URL for your Slack team. It should take the form of :code:`https://your-team.slack.com`. This is also used to create links in your CMS.

:code:`SLACKCHAT_DEFAULT_OWNER`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The Slack user ID for the default owner of new Slack Chats. While the CMS requires that user's be logged in, if the logged-in Django user does not have a matching Slackchat user, this default owner will be set as the owner and invited to any new chats.

Additional config
-----------------

:code:`SLACK_WEBHOOK_VERIFICATION_TOKEN`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A custom token that will be sent in webhook notification post data as :code:`token`. This can be used to verify requests to your renderer's endpoint come from slackchat.

.. code-block:: python

  # default
  SLACK_WEBHOOK_VERIFICATION_TOKEN = 'slackchat'

:code:`SLACKCHAT_PUBLISH_ROOT`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Configuring this to the URL root where your slackchats are published by a renderer will add a direct link to each chat in the :code:`Channel` Django admin.

.. code-block:: python

  # e.g.
  SLACKCHAT_PUBLISH_ROOT = 'https://mysite.com/slackchats/'

:code:`SLACK_MARKSLACK_USER_TEMPLATE`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A function used to create a `user_templates object in markslack <https://github.com/The-Politico/markslack#user-templates>`_. The function should take a :code:`User` instance argument and return a formatted string.

.. code-block:: python

  # default
  SLACK_MARKSLACK_USER_TEMPLATE = lambda user: '<span class="mention">{} {}</span>'.format(
      user.first_name,
      user.last_name
  )

:code:`SLACK_MARKSLACK_LINK_TEMPLATES`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A markslack `link_templates object <https://github.com/The-Politico/markslack#link-templates>`_.

.. code-block:: python

  # default
  SLACK_MARKSLACK_LINK_TEMPLATES = {
        'twitter.com': '<blockquote class="twitter-tweet" data-lang="en"><a href="{}"></a></blockquote>',
    }


:code:`SLACK_MARKSLACK_IMAGE_TEMPLATE`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A markslack `image_template object <https://github.com/The-Politico/markslack#image-template>`_.

.. code-block:: python

  # default
  SLACK_MARKSLACK_IMAGE_TEMPLATE = '<figure><img href="{}" /></figure>'


:code:`SLACKCHAT_USER_IMAGE_UPLOAD_TO`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A function used to set the `upload path <https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.FileField.upload_to>`_ used when copying Slack user profile images to your own server.

.. code-block:: python

  # default
  def default_user_image_upload_to(instance, filename):
      return 'slackchat/users/{0}{1}/{2}'.format(
          instance.first_name,
          instance.last_name,
          filename,
      )

  SLACKCHAT_USER_IMAGE_UPLOAD_TO = default_user_image_upload_to


:code:`SLACKCHAT_MANAGERS`
^^^^^^^^^^^^^^^^^^^^^^^^^^
An array of Slack User IDs. These users will be automatically invited to any new channels made by this app.

.. code-block:: python

  # default
  SLACKCHAT_MANAGERS = []

:code:`SLACKCHAT_CMS_TOKEN`
^^^^^^^^^^^^^^^^^^^^^^^^^^^
A token used to authenticate API requests made by the CMS. Defaults to a random hash created on server startup, but you can use this setting to set it explicitly if you want to use the API endpoint to create/update Channel models.

.. code-block:: python

  # default
  SLACKCHAT_CMS_TOKEN = "%032x" % random.getrandbits(128)
