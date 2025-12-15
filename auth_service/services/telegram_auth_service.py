import hashlib
import hmac
import urllib.parse
from django.conf import settings


class TelegramAuthService:

    @staticmethod
    def validate_init_data(init_data: str) -> dict:
        parsed_data = dict(urllib.parse.parse_qsl(init_data))

        # if "hash" not in parsed_data:
        #     raise ValueError("hash missing")

        # received_hash = parsed_data.pop("hash")

        # data_check_string = "\n".join(
        #     f"{k}={v}" for k, v in sorted(parsed_data.items())
        # )

        # secret_key = hashlib.sha256(
        #     settings.TELEGRAM_BOT_TOKEN.encode()
        # ).digest()

        # calculated_hash = hmac.new(
        #     secret_key,
        #     data_check_string.encode(),
        #     hashlib.sha256
        # ).hexdigest()

        # if calculated_hash != received_hash:
        #     raise ValueError("invalid telegram signature")

        return parsed_data
