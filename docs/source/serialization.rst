Serialization
=============

Channel
-------

Slackchat-serializer includes a RESTful API with a single endpoint used to serialize a channel and all its messages, reactions and users.

You can access the serialized representation for any channel at:

:code:`{slackchat URL}/api/channels/{channel ID}/`

Here's an example of a serialized channel:

.. code-block:: json

  {
    "id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
    "api_id": "GXXXXXXXX",
    "chat_type": "basic",
    "title": "Our first Slackchat!",
    "image": "slackchat/channels/lede-image-234.jpg",
    "introduction": "Welcome to our first Slackchat. \nFollow along below:",
    "meta": {
        "title": "First Slackchat",
        "description": "Live blogging.",
        "keywords": "News, Slackchat"
    },
    "users": {
        "U4XV32XKR": {
            "first_name": "Jon",
            "last_name": "McClure",
            "image": "slackchat/users/JonMcClure/profile-7f37ceefad.jpg",
            "title": "Interactive news editor"
        }
    },
    "messages": [
        {
            "timestamp": "2018-02-04T15:00:45.000065Z",
            "user": "U4XV32XKR",
            "content": "Hi, welcome to our **first** *Slackchat*!",
            "reactions": [],
            "args": ["edited"],
            "kwargs": {
              "style": "moderator-styles"
            }
        },
        {
            "timestamp": "2018-02-04T15:10:09.000129Z",
            "user": "U4XV32XKR",
            "content": "Check out this [link](http://www.google.com).",
            "reactions": [
              {
                "timestamp": "2018-02-04T19:21:29.000085Z",
                "reaction": "fire",
                "user": "U4XV32XKR"
              },
            ],
            "args": [],
            "kwargs": {}
        }
    ]
  }

chat_type
^^^^^^^^^

Slackchats are serialized with a chat_type property, which represents a :code:`ChatType` instance.

This is useful to identify a particular template your renderer may use to render different types of slackchats, for example, using different design treatments or branding.

Custom `args & kwargs`_ patterns are also configured per ChatType.

meta
^^^^

Use meta attributes to fill out social meta tags in your renderer.

messages
^^^^^^^^

Messages are rendered in Markdown syntax by default, unless :code:`render_to_html = True` on the :code:`ChatType` instance, in which case the message is rendered from Markdown into HTML when serializing.

See the `markslack <https://github.com/The-Politico/markslack>`_ package and :ref:`config-options` for more information on how your users can format links, images, user mentions and text in Slack messages.

reactions
^^^^^^^^^

Reactions are captured with the emoji code of the reaction, for example, :code:`fire` for `🔥`.

We recommend using the `emoji <https://pypi.python.org/pypi/emoji/>`_ package to translate reaction emoji codes to true unicode symbols in your renderer, which is what `markslack <https://github.com/The-Politico/markslack#emoji>`_ uses when converting messages from Slack.


args & kwargs
^^^^^^^^^^^^^

With each message you can serialize custom data, which can signal some special handling to your renderer.

Slackchat-serializer lets you construct that data like the arguments and keyword arguments you'd pass to a function. Configure them using the :code:`Argument` and :code:`KeywordArgument` models and then consume them in your renderer.

These features can be used to represent important workflow steps or to add custom metadata to messages.

args
~~~~

Args are most often created through emoji reactions in Slack.

For example, say you want the :code:`:white_check_mark:` ( ✅ ) reaction to signal to your renderer that a message has been copyedited.

You can create an :code:`Argument` object associated with that character -- e.g., :code:`'white_check_mark'` -- with a custom argument name -- e.g., :code:`'edited'` -- that will be serialized with any message with that emoji reaction.

.. image:: ./images/reaction.png
  :width: 300px

.. code-block:: json

  "messages": [
        {
            "timestamp": "2018-02-04T15:00:45.000065Z",
            "user": "SOMEUSER1",
            "content": "My message is ready to publish.",
            "reactions": [],
            "args": ["edited"],
            "kwargs": {}
        },
    ]


You can also use a :code:`CustomContentTemplate` instance to attach an arg to a message whenever the instance's :code:`search_string` matches the content of a message.

kwargs
~~~~~~

Kwargs are created by messages in a thread attached to a Slack message.

Create your threaded message with a key: value pair:

.. image:: ./images/thread.png
  :width: 375px

That pair will parsed and serialized as kwargs on the message:

.. code-block:: json

  "messages": [
        {
            "timestamp": "2018-02-04T15:00:45.000065Z",
            "user": "SOMEUSER1",
            "content": "My message.",
            "reactions": [],
            "args": [],
            "kwargs": {
              "myKey": "Some custom content!"
            }
        },
    ]

One common use case for kwargs is to tag messages for use in custom navigation in the rendered slackchat.


Custom content templates
^^^^^^^^^^^^^^^^^^^^^^^^

You can use a :code:`CustomContentTemplate` to change the way messages' content is serialized or to add a custom arg to a message.

Set a regex :code:`search_string` to match against messages' content and capture groups of any content you want to reformat. Then add a :code:`content_template` Python formatting string that will reformat content.

For example, you might set up a :code:`CustomContentTemplate` instance like this:

.. code-block:: python

  # regex search string
  template.search_string =  '^ALERT! (.*)'

  # formatting string
  template.content_template = '<span class="alert-bold">{0}</span>'

Now a message from Slack like this:

::

  ALERT! New slackchat started!

... would be reformated in the serializer like this:

::

  <span class="alert-bold">New slackchat started!</span>

You can also add an :code:`argument_name` to your template instance, which will place the argument in the matched message's :code:`args` when serialized.

For example ...

.. code-block:: python

  template.argument_name = 'new-section'

... would render like this in the serializer of a matched message:

.. code-block:: json

  "messages": [
        {
            "timestamp": "2018-02-04T15:00:45.000065Z",
            "user": "SOMEUSER1",
            "content": "A matched message",
            "reactions": [],
            "args": ["new-section"],
            "kwargs": {}
        },
    ]


It's up to you to make sure your regex search strings aren't too greedy, but we do feel honor-bound to at least remind you:

  *Some people, when confronted with a problem, think "I know, I'll use regular expressions." Now they have two problems.*

.. note::

  You can turn off kwarg handling for a :code:`ChatType` by setting :code:`kwargs_in_threads = False`.
