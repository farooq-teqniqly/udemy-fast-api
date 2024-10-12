"""
This module provides constants for HTTP status codes used throughout the application.
The codes defined here represent standard response statuses that can be used to improve
code readability and maintainability by avoiding magic numbers in the codebase.

Constants:
- OK: Standard response for successful HTTP requests (200).
- UNPROCESSABLE_ENTITY: Indicates that the server understands the content type of the
  request entity, and the syntax of the request entity is correct, but it was unable
  to process the contained instructions (422).
"""

OK = 200
UNPROCESSABLE_ENTITY = 422
