import asyncio
import json
from datetime import datetime

from .exception import (
    AioAlipayTimeoutError,
    AioAlipayAuthError,
)
from .util import sign_data


class AioAlipayAuth:

    async def get_oauth_token(self, code):
        timestamp = datetime.now()
        params = {
            'app_id': self.app_id,
            'method': 'alipay.system.oauth.token',
            'charset': 'utf-8',
            'sign_type': 'RSA2',
            'version': '1.0',
            'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'grant_type': 'authorization_code',
            'code': code,
        }

        sign = sign_data(self.app_private_key, params)
        params['sign'] = sign

        url = 'https://openapi.alipay.com/gateway.do'

        try:
            async with self._session.get(url, params=params,
                                         timeout=self.timeout) as resp:
                resp_text = await resp.text()
                # print(resp_text)
                result = json.loads(resp_text)
                data = result.get('alipay_system_oauth_token_response')
                if 'code' in data:
                    raise AioAlipayAuthError(result)
                access_token = data.get('access_token')
                user_id = data.get('user_id')
                return access_token, user_id

        except asyncio.TimeoutError:
            raise AioAlipayTimeoutError()

