class ObjectsNotValidatedError(Exception):
    """docstring fo NotValidatedError."""

    def __init__(self,not_validated=None):
        if not_validated:self.not_validated = list(not_validated)

    def __str__(self):
        return f"The following have not checked out:{' '.join(self.not_validated)}"
