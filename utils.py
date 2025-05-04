from functools import wraps
import pprint, logger

def _inner_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.logger.info(f"Inner call {func.__qualname__} with args \n\t{pprint.pformat(args)} \n\tand kwargs {pprint.pformat(kwargs)}, \n\treturns {pprint.pformat(result)}.")
        return result
    
    return wrapper