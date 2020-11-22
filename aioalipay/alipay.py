import aiohttp
from Crypto.PublicKey import RSA

from .auth import AioAlipayAuth


class AioAlipay(AioAlipayAuth):

    def __init__(self, app_id, private_key_path, timeout=5):
        """
        :param app_id:
        :param private_key_path:
        :param timeout: request timeout
        """
        conn = aiohttp.TCPConnector(limit=1024)
        self._session = aiohttp.ClientSession(
            connector=conn,
            skip_auto_headers={'Content-Type'},
        )
        self.app_id = app_id
        with open(private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())
        self.timeout = timeout

    def __del__(self):
        if not self._session.closed:
            if self._session._connector is not None \
                    and self._session._connector_owner:
                self._session._connector.close()
            self._session._connector = None
