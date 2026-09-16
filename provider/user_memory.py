from typing import Any
from dify_plugin import ToolProvider


class UserMemoryProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # The plugin has no external credentials or network dependency.
        return None
