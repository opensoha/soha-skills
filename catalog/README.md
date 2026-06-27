# Skill Catalog

This catalog is a packaged release asset. It records the Gateway capability
snapshot consumed by official OpenSoha skills and the compatibility matrix used
by local validation.

## Compatibility Matrix

- Skills package version: `0.1.0`
- Gateway capability catalog version: `0.1.0`
- Platform capability catalog version: `0.1.0`
- Supported `soha-core`: `>=0.1.0 <0.2.0`
- Supported `soha-cli`: `>=0.1.0 <0.2.0`
- Supported `soha-agent`: `>=0.1.0 <0.2.0`

The normalized Gateway required scope union is:

- `application`
- `aiClient`
- `approval`
- `audit`
- `businessLine`
- `cluster`
- `deployment`
- `environment`
- `executionTask`
- `namespace`
- `node`
- `pod`
- `policy`
- `relayCache`
- `relayCall`
- `relayRoute`
- `relayUpstream`
- `releaseBundle`
- `repository`
- `service`
- `serviceAccount`
- `skill`
- `storage`
- `subject`
- `timeRange`
- `token`
- `tool`

Validation prefers the published `node_modules/@opensoha/contracts` package
when it is available. A sibling `../soha-contracts` checkout is a local
development fallback before public release artifacts are published.

The packaged contract schema locations are:

- `node_modules/@opensoha/contracts/skills/skill-manifest.schema.json`
- `node_modules/@opensoha/contracts/presets/mcp-preset.schema.json`
- `node_modules/@opensoha/contracts/profiles/agent-profile.schema.json`
- `../soha-contracts/skills/skill-manifest.schema.json`
- `../soha-contracts/presets/mcp-preset.schema.json`
- `../soha-contracts/profiles/agent-profile.schema.json`

[`asset-governance.json`](./asset-governance.json) records release signing
requirements, permission review coverage for every packaged skill, MCP preset,
and agent profile, and the install audit event schema required for verify,
install, upgrade, rollback, and activate decisions.

Install the versioned wrapper package and expand the matching raw skills
runtime into a staging directory under `~/.soha/skills`. Upgrade only after the
release manifest, checksum, compatibility matrix, validation report, and target
CLI load check pass. Roll back by restoring the previous verified wrapper
package and switching the active `~/.soha/skills` runtime pointer back to the
previous verified directory.
