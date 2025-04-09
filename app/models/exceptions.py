class PostError(Exception):
    """Base exception for post-related errors."""
    pass

class PostNotFoundError(PostError):
    """Raised when a post cannot be found."""
    pass

class PostMetadataError(PostError):
    """Raised when there's an error with post metadata."""
    pass

class PostContentError(PostError):
    """Raised when there's an error with post content."""
    pass

class YAMLParsingError(PostError):
    """Raised when there's an error parsing YAML front matter."""
    pass

class MarkdownRenderingError(PostError):
    """Raised when there's an error rendering markdown content."""
    pass 