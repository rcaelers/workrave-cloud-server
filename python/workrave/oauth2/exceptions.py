class OAuthError(Exception):
    def __init__(self, error, detail):
        self.error = error
        self.detail = detail
