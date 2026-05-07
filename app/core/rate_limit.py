from slowapi import Limiter
from slowapi.util import get_remote_address

# Global default limit is set, but can be overridden on specific endpoints
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
