class NotFoundError(Exception):
    """Exception raised when a requested resource is not found."""
    pass

class BadIncludeError(Exception):
    """Exception raised for invalid include parameters."""
    pass

class PlayerNameConflictError(Exception):
    """Exception raised when there is a conflict with player names."""
    pass

class PlayerColorConflictError(Exception):
    """Exception raised when there is a conflict with player colors."""
    pass