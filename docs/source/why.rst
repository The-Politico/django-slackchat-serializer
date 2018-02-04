Why this?
=========

Slack is a great platform for liveblogging and creating custom threaded content. In the newsroom, we use it to cover live events and to break out features that take advantage of a more conversational tone.

There are two steps to publishing a slackchat. The first is to serialize the messages, reactions and threads you get from Slack into some data you can use to render a custom page. The second is to use that data to render the conversation on the page with whatever design conventions you choose and publish it wherever you need.

We separate those two concerns at POLITICO. Django-slackchat-serializer focuses on the former. It creates a rich, serialized representation of a conversation in Slack, including custom metadata you can add to individual messages.

Separating the serializer allows you to integrate it with your own custom renderer. To make the integration easy, slackchat-serializer throws off webhooks so your renderer can subscribe to updates and react accordingly, especially when publishing live.

Upshot, if you're looking to setup a slackchat system, this app removes the complexity of integrating with Slack so you can focus on the page design and business logic you need to publish your custom page or render within your CMS.
