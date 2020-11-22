
class AioAlipayError(Exception):
    pass


class AioAlipayTimeoutError(AioAlipayError):
    pass


class AioAlipayAuthError(AioAlipayError):
    pass
