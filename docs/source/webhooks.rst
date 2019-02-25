Webhooks
========

Slackchat-serializer will fire webhooks whenever :code:`Message`, :code:`Reaction`, :code:`Attachment` or :code:`KeywordArgument` objects are saved or deleted.

Verifying your endpoint
-----------------------

Slackchat asks to verify your endpoint before it will send notifications.

To do so, it will send a payload that looks like this:

.. code-block:: json

  {
    "token": "your-webhook-verification-token",
    "type": "url_verification",
    "challenge": "a-challenge",
  }

You endpoint should sniff the :code:`type` and reply back with the challenge.

For example, you could use Django Rest Framework in a view to respond to the challenge like this:

.. code-block:: python

  class Webhook(APIView):
      def post(self, request, *args, **kwargs):
          payload = request.data

          if payload.get('token') != WEBHOOK_VERIFICATION_TOKEN:
              return Response(status=status.HTTP_403_FORBIDDEN)

          if payload.get('type') == 'url_verification':
              return Response(
                  data=payload.get('challenge'),
                  status=status.HTTP_200_OK
              )
          # Now handle regular notifications...

.. note::

  If you need to fire a repeat verification request because your endpoint didn't respond correctly the first time or because the endpoint URL changed, simply open the :code:`Webhook` instance in Django's admin and re-save it.

Update Payload
--------------

Whenever one of the notification models is updated, the app will send a payload to every verified endpoint with the ID of the channel that was updated, allowing your renderer to hit the channel's API and republish the updated data.

.. code-block:: json

  {
    "token": "your-webhook-verification-token",
    "type": "update_notification",
    "channel": "a-channel-uuid-xxxx...",
    "chat_type": "a-chat-type"
  }

If the type of the webhook is :code:`update_notification`, the payload will also include an :code:`update_type` of :code:`message_created`, :code:`message_changed`, or :code:`message deleted`. It will also include a :code:`message` key with data about the message that was added, changed, or deleted.

.. code-block:: json

  {
    "token": "your-webhook-verification-token",
    "type": "update_notification",
    "channel": "a-channel-uuid-xxxx...",
    "chat_type": "a-chat-type"

    "update_type": "message_added",
    "message": {
      "timestamp": "2018-10-16T17:23:49.000100Z",
      "user": "USERID",
      "content": "A new message."
    }
  }


Explicit Payloads
-----------------

Users can also use the Django admin or CMS to send endpoints explicit request payloads.

:code:`republish_request`
^^^^^^^^^^^^^^^^^^^^^^^^^

A request to publish (or republish) all static assets associated with the channel. It carries with it the channel data as a serialized JSON string.

.. code-block:: json

  {
    token: "your-webhook-verification-token",
    type: "republish_request",
    channel: "a-channel-uuid-xxxx...",
    channel_data: "{ ... \"title\": \"Channel Title\", \"introduction\": \"Lorem ipsum\", ... }",
    chat_type: "a-chat-type"
  }

:code:`unpublish_request`
^^^^^^^^^^^^^^^^^^^^^^^^^

A request to unpublish (or otherwise remove) all static assets associated with the channel. It carries with it the channel data as a serialized JSON string.

.. code-block:: json

  {
    token: "your-webhook-verification-token",
    type: "unpublish_request",
    channel: "a-channel-uuid-xxxx...",
    channel_data: "{ ... "title": "Channel Title", "introduction": "Lorem ipsum", ... }",
    chat_type: "a-chat-type"
  }
