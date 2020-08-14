class ObjectsNotValidatedError(Exception):
    """
        Checks for objects that have not been validated
    """

    def __init__(self, not_validated=None):
        if not_validated:
            self.not_validated = list(not_validated)

    def __str__(self):
        invalid = ' '.join(self.not_validated)
        return f"The following have not checked out:{invalid}"
