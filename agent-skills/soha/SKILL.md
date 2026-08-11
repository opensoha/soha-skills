---
name: soha
description: Use when an AI agent needs to configure Soha MCP or skills, inspect OpenSoha capabilities, create a Soha-compliant application service, or plan, publish, update, verify, and roll back releases through the governed delivery center.
---

# Soha

Use Soha as the control plane for delivery-center work. Prefer the configured Soha MCP server. Use the `soha` CLI when MCP is unavailable or when the task is installation, diagnostics, or explicit command-line automation.

## Connect

1. Check `soha version --json`, `soha profile list`, and `soha context show`.
2. Configure the current agent with `soha setup --client <client> --mode both`. Use `--scope project` only when the repository should own the agent configuration; the default is user scope. Add `--base-url <url>` only for a self-hosted Soha deployment; otherwise the official SaaS endpoint is used.
3. When `soha` is not installed and `@opensoha/cli` is available in the npm registry, use `npx -y @opensoha/cli@latest setup --client <client> --mode both` for a verified one-shot bootstrap. If npm returns `E404`, use the native Soha CLI release because the npm launcher has not been published yet.
4. Validate an existing installation with `soha setup --client <client> --check`. Use `soha skill status`, `soha skill update`, and `soha skill rollback` for runtime skill lifecycle; do not invent or request a `--skills-version` flag.
5. Never request a token in chat. Ask the user to run `soha login` or set `SOHA_TOKEN` outside the conversation when authentication is missing.

## Discover

1. Treat the live MCP tool list as authoritative.
2. With the CLI, run `soha capabilities --output names`, then `soha capabilities --output inputs` before an unfamiliar call.
3. Use `soha diagnose --tool <name>` when a capability, permission, scope, skill binding, or approval path is unclear.
4. Read `references/skills/index.json` and the relevant file under `references/skills/` before a product workflow. For delivery-center work, start with `delivery-developer.md`.

## Diagnose Kubernetes

1. Select the `k8s-sre` skill with the `k8s-readonly` MCP preset and verify the live tool inputs before collecting evidence. With the CLI, run `soha context set --skill-id k8s-sre`, `soha capabilities --output inputs`, and `soha diagnose --tool k8s.pods.logs --resource soha://k8s/runtime`.
2. Keep `clusterId`, `namespace`, workload identity, and time range explicit. Use only the K8s tools, resources, and prompts visible in the current Gateway manifest; do not infer availability from a catalog or skill document.
3. Stay read-only. Correlate namespace and workload summaries, rollout status, events, pod state, bounded logs, service backends, routes, storage, node conditions, and metadata-only ConfigMap, Secret, or Helm release results, then separate confirmed evidence from hypotheses.
4. Report permission failures, agent parity gaps, and `capabilityWarnings` as evidence limitations. Do not fall back to kubeconfig, `kubectl`, exec, port-forward, restart, scale, rollback, patch, or delete.

## Use Secrets

1. Never request or place a secret value in chat, tool business input, plans, manifests, logs, or generated files. Ask the user to create or rotate it with the hidden-input `soha secret` commands or the Web Secret Store.
2. Select canonical references with `soha secret list` or the Web console. Use aliases matching `[A-Z_][A-Z0-9_]*` and references shaped as `soha://secrets/{id}` or `soha://secrets/{id}/versions/{version}`.
3. For MCP calls, attach the alias-to-reference map through the reserved `_sohaSecretRefs` argument. The Soha adapter removes it from business input and sends canonical top-level `secretRefs`.
4. For direct CLI tool calls, repeat `--secret-ref ALIAS=soha://secrets/{id}`. Keep the same references between a plan and its approved execution.
5. Secret use remains subject to `secret.use`, scope and binding checks, approval, and audit. Remote agents redeem an opaque, short-lived, one-time lease; agents never receive the stored reference or reusable credentials.

## Create An Application Service

1. List applications and avoid creating a duplicate.
2. Gather only non-secret repository and ownership metadata: application name and key, business line, owner, repository, language, service components, build source, environments, release targets, and workflow intent.
3. Analyze the repository with the visible onboarding capability.
4. Generate and validate Dockerfile, Helm, or Kubernetes standards only through visible Soha delivery capabilities.
5. Render or bootstrap the delivery specification, then create a delivery draft.
6. Show the draft, validation findings, affected services and environments, and approval requirements. Stop for explicit confirmation.
7. Confirm the draft only after the user approves it. Preserve returned application, service, environment, build-source, and release-target IDs.

## Publish Or Update

1. Read application detail, services, environment bindings, build sources, release targets, and the current release context.
2. Create a release plan for the requested build, deploy, build-deploy, workflow, verify, update, or rollback action.
3. State the target environment, branch or commit, release bundle, diff, risks, and approvals before persisting or confirming the plan.
4. Confirm a plan only after explicit user approval. If Soha returns an approval handoff, stop and report it instead of retrying around governance.
5. Follow execution tasks, redacted logs, artifacts, verification results, and release status until a clear terminal or handoff state.
6. For rollback, read rollback context first and confirm the exact release bundle and reason.

## Guardrails

- Do not bypass Soha with direct Kubernetes, CI, runner, database, registry, or deployment-target commands.
- Do not expose access tokens, refresh tokens, passwords, private keys, kubeconfig, registry credentials, environment secrets, or unredacted secret-looking logs.
- Do not put secret references in normal capability input or attempt to resolve them outside Soha.
- Do not invent capability names, IDs, schemas, permissions, or successful outcomes.
- Do not perform a mutation merely because a tool is available. Require clear user intent and honor preview, confirmation, approval, and audit boundaries.
- Keep business line, application, service, environment, branch, commit, release bundle, execution task, and approval IDs explicit in the final handoff.
