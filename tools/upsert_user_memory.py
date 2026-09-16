import json
from collections.abc import Generator
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from tools.memory_store import ALLOWED, load, save


class UpsertUserMemoryTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        user_id = str(tool_parameters.get("user_id", "")).strip()
        try:
            request = json.loads(str(tool_parameters.get("memory_json", "")))
        except json.JSONDecodeError:
            yield self.create_variable_message("result", '{"stored":false,"reason":"invalid_json"}')
            return
        key, value = str(request.get("key", "")), " ".join(str(request.get("value", "")).split())
        if not user_id or request.get("should_store") is not True or request.get("explicit") is not True or key not in ALLOWED or not value or len(value) > 120:
            yield self.create_variable_message("result", '{"stored":false}')
            return
        data = load(self.session.storage, user_id)
        data["facts"][key] = {"value": value, "explicit": True}
        save(self.session.storage, user_id, data)
        yield self.create_variable_message("result", json.dumps({"stored": True, "memory": {key: value}}, ensure_ascii=False))
