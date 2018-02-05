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


:code:`Argument`
----------------

An argument that can be attached to a message through an emoji reaction in Slack. Arguments can signal some sort of special handling for the message in a renderer.

:code:`KeywordArgument`
-----------------------

A keyword argument that can be attached to a message through a threaded message. Keyword arguments can signal some sort of special handling for the message in a renderer.

:code:`CustomContentTemplate`
-----------------------------

A template that matches a regex pattern against a message's content and can be used to reformat that content or to attach an argument when a match is found.
