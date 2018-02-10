Models
======

:code:`ChatType`
----------------

A type of slackchat.


:code:`Channel`
---------------

A channel that hosts a slackchat.

:code:`User`
------------

A participant in a slackchat.

:code:`Message`
---------------

A message posted by a user in a Slack channel.

:code:`Reaction`
----------------

An emoji reaction to a message in Slack.

:code:`Attachment`
------------------

An unfurled link or media item attached to a message.


:code:`Argument`
----------------

An argument that can be attached to a message through an emoji reaction in Slack. Arguments can signal to a render that a message should be handled in a special way.

:code:`KeywordArgument`
-----------------------

A keyword argument that can be attached to a message through a threaded message. Keyword arguments can signal to a render that a message should be handled in a special way.

:code:`CustomContentTemplate`
-----------------------------

A template that matches a regex pattern against a message's content and can be used to reformat that content or to attach an argument when a match is found.
