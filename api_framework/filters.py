
class BaseFilterBackend:
    """
    A base class from which all filter backend classes should inherit.
    """

    def filter_modelselect(self, request, modelselect, controller):
        """
        Return a filtered queryset.
        """
        raise NotImplementedError(".filter_modelselect() must be overridden.")

    def get_schema_fields(self, view):
        return []

    def get_schema_operation_parameters(self, view):
        return []

