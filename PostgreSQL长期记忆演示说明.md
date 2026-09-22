# PostgreSQL 长期记忆演示

这份演示使用 Dify Chatflow、内部 Memory API 和 Azure PostgreSQL。Chatflow 不直接连接数据库。

```text
Dify Chatflow → Memory API → Azure PostgreSQL
```

## 流程

```text
开始（填写测试用户 ID）
  → 召回长期记忆
  → FAQ / 数据查询识别
  → FAQ 知识库检索，或抽取指标、年份、地区
  → 缺少地区时追问，用户补充后继续查询
  → 基于知识库证据回复
  → 提取默认地区、身份、称呼
  → 通过 Memory API 写入 PostgreSQL
```

## Chatflow 需要配置的内容

1. 在环境变量 `MEMORY_API_BASE_URL` 填入内部 Memory API 地址。
2. 在两个知识检索节点分别绑定 FAQ 知识库和金融数据知识库。
3. 将所有模型节点改为当前 Dify 已配置的模型。
4. 测试时，开始节点填写固定的测试用户 ID，例如 `demo-xiaowang`。

## Memory API 接口约定

### 读取记忆

```text
GET /v1/memories/search?user_id=demo-xiaowang&query=2023 年 VONB 是多少？&top_k=3
```

响应示例：

```json
{
  "user_id": "demo-xiaowang",
  "memories": [
    {"memory_key": "default_region", "memory_value": "华东"},
    {"memory_key": "user_role", "memory_value": "区域负责人"},
    {"memory_key": "preferred_name", "memory_value": "小王"}
  ]
}
```

### 写入记忆

```text
POST /v1/memories/upsert
Content-Type: application/json
```

```json
{
  "user_id": "demo-xiaowang",
  "items": [
    {"memory_key": "default_region", "memory_value": "华东"}
  ]
}
```

允许写入的字段只有 `default_region`、`user_role` 和 `preferred_name`。

## 演示步骤

1. 填写测试用户 ID：`demo-xiaowang`。
2. 输入：“我叫小王，是华东区域负责人，以后默认查询华东地区。”
3. 新开对话，仍填写 `demo-xiaowang`。
4. 输入：“2023 年 VONB 是多少？”
5. Chatflow 读取默认地区“华东”，检索知识库后回答；如果知识库没有数据，会说明数据不足，不会编造。
