# Privacy

This plugin stores only user facts that the user explicitly provides and the Chatflow marks as explicit. Storage is isolated by Dify workspace and plugin installation.

Allowed fields are origin or residence region, work region, user role, default query region, language, default currency, and reporting preference. The plugin has no network permission and no credentials. It does not store passwords, IDs, payment data, health information, model inferences, or one-time queries.

Users can request deletion through the `forget_user_memory` tool. Workspace administrators are responsible for retention policy and plugin-storage backups under their enterprise Dify deployment.
