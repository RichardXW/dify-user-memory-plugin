# 用户长期记忆 Dify 插件

此插件是 Dify `1.9.0+` 的无外部依赖长期记忆方案。它使用 Dify Plugin Daemon 内置的持久化 KV 存储；不需要 MySQL、Redis、外部 HTTP 地址或 API Key。

## 为什么替代外部 JSON API

跨新会话记忆必须有持久化存储。Dify Chatflow 的 Conversation Variables 只在同一 conversation id 内有效。此插件将持久化存储放在 Dify 自己的 Plugin Daemon 中，KV 数据按“工作区 + 插件安装”隔离，因此企业 Dify 无须访问外部 Memory API。

## 三个工具

| 工具 | Chatflow 用途 |
|---|---|
| `recall_user_memory` | 首节点读取指定 `user_id` 的明确偏好与画像，并注入后续提示词 |
| `upsert_user_memory` | 仅保存用户明确说出的稳定事实 |
| `forget_user_memory` | 用户明确要求删除时按字段删除记忆 |

允许保存字段：`origin_region`、`residence_region`、`work_region`、`user_role`、`default_region`、`language`、`default_currency`、`response_preference`。

例如“我是上海人”应写入 `origin_region=上海`；“我住在杭州”应写入 `residence_region=杭州`；“默认地区是华东”应写入 `default_region=华东`。这三个含义不可混用。

## 安装

1. 在 Dify 的插件页面选择“通过本地文件安装”。
2. 上传交付根目录的 `dify-user-memory-v0.1.0.difypkg`。
3. 安装成功后，插件不要求配置任何凭据、地址或 Key。
4. 在 Chatflow 中新增三个工具节点并选择本插件的对应工具。

## Chatflow 接线

```text
Start
  -> recall_user_memory(user_id = sys.user_id)
  -> FAQ / 业务问题分类
  -> 业务问题时：参数抽取 + 8轮短期记忆 + 缺参追问 + 知识检索
  -> 回答
  -> LLM 抽取明确长期记忆 JSON
  -> upsert_user_memory(user_id = sys.user_id)
```

`recall_user_memory.memory_context` 必须注入到“路由”“参数抽取”和“最终回答”节点。参数抽取规则：若用户本轮没有指定地区，才可使用 `default_region`；用户本轮明确地区必须覆盖长期记忆。

保存前的 LLM 应严格输出：

```json
{"should_store":true,"explicit":true,"key":"default_region","value":"华东"}
```

模型推测、一次性问题、联系方式、身份证号、账号、健康信息都必须输出 `should_store:false`。

## 演示与生产边界

- 演示：该插件足以实现新开会话后记住“默认查询华东”“来自上海”“中文回答”等事实。
- 生产初期：KV 隔离和白名单校验适合低并发的稳定偏好；开启企业 Dify 的插件备份、审计和最小权限管理。
- 生产规模化：当需要大量历史事实、语义检索、细粒度授权、跨工作区共享或高并发时，再迁移到企业数据库和专用 Memory Service。Chatflow 的读写契约应保持不变。

## 客户演示用例

1. 用户：“我是上海人，默认查询华东地区，请记住。”
2. 新会话，保持同一个 Dify API `user` 值。
3. 用户：“2023 年 VONB 是多少？”
4. 机器人读取 `origin_region=上海` 与 `default_region=华东`，按华东地区检索并基于知识库作答。
5. 用户：“改查上海。”
6. 机器人以本轮“上海”覆盖默认地区，仅本次查询使用上海；如用户明确说“以后默认上海”，再更新长期记忆。

## 已知限制

- Dify 的内置 KV 按工作区和插件安装隔离，不能跨工作区共享。
- 使用网页匿名聊天时，要保证前端或 API 为同一客户提交稳定的 `user` 值；否则无法判断“是不是同一个人”。
- 本交付已完成静态 Python 编译与包结构检查；必须在企业 Dify 测试工作区完成一次本地文件安装和工具节点联调后才可生产上线。
