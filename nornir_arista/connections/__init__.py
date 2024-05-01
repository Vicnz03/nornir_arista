from typing import Any, Dict, Optional
import pyeapi
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
        connection = pyeapi.connect(return_node=True,**parameters)
        self.connection = connection

    def close(self) -> None:
        pass