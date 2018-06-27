# Stdlib imports
# Core Django imports
# Third-party app imports
# Imports from your apps


# This class will create the standard retry decorator.
# It only retries on a 500 status code.
class Retry:
    # By default, retry up to this many times.
    MAX_TRIES = 3

    # This method holds the validation check.
    def is_valid(self, resp):
        # By default, only retry if a status code is 500.
        return resp.status_code == 500

    def __call__(self, func):
        def retried_func(*args, **kwargs):
            tries = 0
            while True:
                resp = func(*args, **kwargs)
                if self.is_valid(resp) or tries >= self.MAX_TRIES:
                    break
                tries += 1
            return resp

        return retried_func


# This will retry on 4xx failures only.
class RetryOnAuthFailure(Retry):
    def is_valid(self, resp):
        return not ((resp.status_code >= 400) and (resp.status_code < 500))


# This will retry on *any* 5xx error, and do so up to 5 times.
class RetryOnServerError(Retry):
    MAX_TRIES = 5

    def is_valid(self, resp):
        return resp.status_code < 500


retry_on_500 = Retry()
retry_on_auth_failure = RetryOnAuthFailure()
retry_on_server_error = RetryOnServerError()
