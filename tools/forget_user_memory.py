import json
from collections.abc import Generator
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from tools.memory_store import ALLOWED, load, save


class ForgetUserMemoryTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        user_id, key = str(tool_parameters.get("user_id", "")).strip(), str(tool_parameters.get("key", "")).strip()
        if not user_id or key not in ALLOWED:
            yield self.create_variable_message("result", '{"deleted":false}')
            return
        data = load(self.session.storage, user_id)
        deleted = data["facts"].pop(key, None) is not None
        save(self.session.storage, user_id, data)
        yield self.create_variable_message("result", json.dumps({"deleted": deleted, "key": key}, ensure_ascii=False))
