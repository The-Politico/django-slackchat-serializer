Webhooks
========

Slackchat-serializer will fire webhooks whenver :code:`Message`, :code:`Reaction` or :code:`KeywordArgument` objects are saved or deleted.

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

  If you need to fire a repeat verification request because your endpoint didn't respond correctly the first time or its URL changed, simply open the :code:`Webhook` instance in Django's admin and re-save it.

Payload
-------

The webhook will send a payload with the ID of the channel that was updated, allowing your renderer to hit the channel's API and republish the updated data.

.. code-block:: json

  {
    "token": "your-webhook-verification-token",
    "type": "update_notification",
    "channel": "a-channel-uuid-xxxx...",
  }
