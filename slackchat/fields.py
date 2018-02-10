# Scandalously stolen from https://github.com/onepill/django-simplemde
from django.contrib.admin import widgets as admin_widgets
from django.db.models import TextField

from .widgets import MarkdownEditorWidget


class MarkdownField(TextField):
    def __init__(self, *args, **kwargs):
        self.widget = MarkdownEditorWidget()
        super(MarkdownField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'widget': self.widget}
        defaults.update(kwargs)

        if defaults['widget'] == admin_widgets.AdminTextareaWidget:
            defaults['widget'] = self.widget
        return super(MarkdownField, self).formfield(**defaults)
