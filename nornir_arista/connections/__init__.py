from typing import Any, Dict, Optional
import pyeapi
import ssl
from nornir.core.configuration import Config

CONNECTION_NAME = "nornir_arista"

class nornir_arista:
    def open(
        self,
        hostname: Optional[str],
        username: Optional[str],
        password: Optional[str],
        port: Optional[int],
        platform: Optional[str],
        extras: Optional[Dict[str, Any]] = None,
        configuration: Optional[Config] = None,
    ) -> None:
        extras = extras or {}

        parameters: Dict[str, Any] = {
            "name": hostname,
            "host": hostname,
            "username": username,
            "password": password,
            "transport": "https",
        }
        parameters.update(extras)
        
        if parameters['transport'] == 'https':
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            context.set_ciphers('AES256-SHA:DHE-RSA-AES256-SHA:AES128-SHA:DHE-RSA-AES128-SHA')
            parameters['context'] = context
        
        connection = pyeapi.connect(return_node=True,**parameters)
        self.connection = connection

    def close(self) -> None:
        pass