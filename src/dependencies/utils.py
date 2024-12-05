import hashlib
import hmac
import urllib.parse
import time
import json
from typing import Any
from .exceptions import DataOutdatedError, InitDataHashMismatch


def check_auth_date(auth_date: int) -> None:
    MAX_DATA_AGE = 5 * 60
    current_time = int(time.time())

    if current_time - auth_date > MAX_DATA_AGE:
        raise DataOutdatedError(auth_date=auth_date, current_time=current_time)
    

def check_init_data(init_data: str, bot_token: str) -> None | dict[str, Any]:
    params = dict(urllib.parse.parse_qsl(init_data))
    received_hash = params.pop('hash', None)
    auth_date = int(params.get('auth_date', 0))

    check_auth_date(auth_date)

    data_check_string = '\n'.join(
        f"{key}={value}" for key, value in sorted(params.items())
    )

    secret_key = hmac.new(
        key = b"WebAppData",
        msg = bot_token.encode('utf-8'),
        digestmod = hashlib.sha256
    ).digest()

    calculated_hash = hmac.new(
        key = secret_key,
        msg = data_check_string.encode('utf-8'),
        digestmod = hashlib.sha256
    ).hexdigest()

    if calculated_hash != received_hash:
        raise InitDataHashMismatch()
    
    return json.loads(params['user'])
