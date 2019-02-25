import uuid

from django.forms import widgets
from django.utils.safestring import mark_safe


class MarkdownEditorWidget(widgets.Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        if "class" not in attrs.keys():
            attrs["class"] = ""

        attrs["class"] += " markdown-editor"

        attrs["data-uuid"] = str(uuid.uuid4())

        html = super(MarkdownEditorWidget, self).render(
            name, value, attrs, renderer
        )

        return mark_safe(html)

    class Media:
        js = (
            "https://cdnjs.cloudflare.com/ajax/libs/simplemde/1.11.2/simplemde.min.js",  # noqa: E501
            "slackchat/js/editor.js",
        )

        css = {
            "all": (
                "https://cdnjs.cloudflare.com/ajax/libs/simplemde/1.11.2/simplemde.min.css",  # noqa: E501
                "slackchat/css/editor.css",
            )
        }
