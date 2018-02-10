from collections import OrderedDict


class NoNonNullMixin(object):
    """Removes fields that are empty or null."""
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        retained = filter(lambda x: x[1], representation.items())
        return OrderedDict(retained)
