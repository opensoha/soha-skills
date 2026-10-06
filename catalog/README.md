# Skill Catalog

This catalog is a packaged release asset. It records the Gateway capability
snapshot consumed by official OpenSoha skills and the compatibility matrix used
by local validation.

## Compatibility Matrix

- Skills package version: `0.1.3`
- Gateway capability catalog version: `0.1.1`
- Platform capability catalog version: `0.1.0`
- Supported `soha-core`: `>=0.1.0 <0.2.0`
- Supported `soha-cli`: `>=0.1.0 <0.2.0`
- Supported `soha-agent`: `>=0.1.0 <0.2.0`

The normalized Gateway required scope union is:

- `application`
- `applicationEnvironment`
- `aiClient`
- `approval`
- `audit`
- `businessLine`
- `cluster`
- `computeDomain`
- `computeResource`
- `computeTask`
- `dataSource`
- `deployment`
- `device`
- `dockerHost`
- `dockerOperation`
- `dockerProject`
- `dockerService`
- `enrollment`
- `environment`
- `executionTask`
- `gateway`
- `grant`
- `namespace`
- `node`
- `pod`
- `policy`
- `producer`
- `relayCache`
- `relayCall`
- `relayRoute`
- `relayUpstream`
- `releaseBundle`
- `repository`
- `resource`
- `runtime`
- `service`
- `serviceAccount`
- `session`
- `site`
- `skill`
- `storage`
- `subject`
- `timeRange`
- `token`
- `tool`
- `virtualizationConnection`
- `vm`
- `workerPool`

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

Worker supply adds the `workerPool` scope alongside the virtualization connection and target cluster. Discover registered pools and their revisions before creation; follow the original VM operation and fresh worker assessment for recovery. The catalog lists source capabilities and is not proof that a running server has upgraded or a provider is ready.

The four CRD/custom-resource and workload metric entries reflect the reviewed Core 0.1.10 tool definitions. Discover capabilities from the running server before invoking them; older supported versions may not expose these tools.
