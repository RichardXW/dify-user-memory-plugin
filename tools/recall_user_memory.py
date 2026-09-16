from collections.abc import Generator
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from tools.memory_store import ALLOWED, load


class RecallUserMemoryTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        user_id = str(tool_parameters.get("user_id", "")).strip()
        if not user_id:
            yield self.create_variable_message("memory_context", "{}")
            return
        facts = load(self.session.storage, user_id)["facts"]
        context = {k: v["value"] for k, v in facts.items() if k in ALLOWED and v.get("explicit") is True}
        yield self.create_variable_message("memory_context", __import__("json").dumps(context, ensure_ascii=False))
