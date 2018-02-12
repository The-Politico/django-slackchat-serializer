Integrating with a renderer
===========================

Slackchat-serializer generally doesn't enforce any conventions as to how you render a slackchat on a custom page or within your CMS.

That said, we recommend that you **do not** let readers hit the serializer API directly, but rather respond to webhooks from the app by republishing the data to a JSON file on a static file server like Amazon Web Services S3.

CORS
----

If you need to allow cross-origin requests in your renderer, we recommend using `django-cors-headers <https://github.com/ottoyiu/django-cors-headers>`_ in your project.
