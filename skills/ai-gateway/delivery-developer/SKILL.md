---
id: delivery-developer
name: Delivery Developer
version: 0.1.0
category: delivery
description: Developer delivery workflows through Soha AI Gateway.
capabilityRefs:
  - delivery.applications.list
  - delivery.applications.detail
  - delivery.applications.create
  - delivery.onboarding.analyze_repo
  - delivery.standards.dockerfile.generate
  - delivery.standards.dockerfile.validate
  - delivery.standards.helm.generate
  - delivery.standards.k8s.validate
  - delivery.spec.render
  - delivery.application.bootstrap
  - delivery.application_environments.list
  - delivery.application_services.list
  - delivery.build_sources.list
  - delivery.release_targets.list
  - delivery.release_bundles.list
  - delivery.execution_tasks.list
  - delivery.execution_logs.list
  - delivery.release.plan
  - delivery.release_context.diff
  - delivery.rollback.context
  - delivery.actions.trigger
requiredScopes:
  - businessLine
  - application
  - environment
---

# Delivery Developer

Use this skill when an AI coding tool is helping a developer onboard an application, review delivery context, or trigger self-service build, deploy, build_deploy, workflow, verify, or controlled rollback actions through soha AI Gateway.

## Operating Contract

- Treat soha as the source of truth for applications, environments, release bundles, execution tasks, approvals, and audit.
- Use Gateway tools only through the MCP tool list returned by the current identity.
- Never call Kubernetes, PostgreSQL, Docker, CI runners, or deployment targets directly.
- Keep build, deploy, verify, workflow, and rollback actions inside `delivery.actions.trigger`; do not synthesize runner callbacks.
- For application onboarding, produce or submit a `DeliveryDraft` only. A draft may include application metadata, service components, build sources, environment bindings, release targets, Dockerfile, Helm/Deployment, workflow template, and approval hints, but it must not create platform objects until a human confirms the draft.
- Preserve application, business line, environment, branch, commit, release bundle, and execution task identifiers in the final answer.

## Workflow

1. Read capabilities and confirm the required delivery tools are visible.
2. List matching applications before creating a new one.
3. For application onboarding, ask for or infer only non-secret metadata: name, key, business line, owner, repository path, language, service names, build source, environment binding, release targets, and workflow template intent.
4. For repository onboarding, use `delivery.onboarding.analyze_repo`, then `delivery.standards.dockerfile.generate` / `delivery.standards.helm.generate` and validation tools as needed.
5. Render onboarding output with `delivery.spec.render` or `delivery.application.bootstrap`; submit a `DeliveryDraft` only through the platform draft API, then stop for human preview confirmation.
6. Do not confirm a `DeliveryDraft` unless the user explicitly approves the preview and the visible Gateway/API capability performs the confirmation.
7. For build, deploy, workflow, verify, or rollback intent, use `delivery.release.plan` first and treat it as a `DeliveryPlan` preview.
8. Query application detail, services, build sources, and environment bindings before triggering any action.
9. For build or deploy actions, include the target application environment, build source, branch or commit, and a short reason.
10. Before rollback, read `delivery.rollback.context`, confirm the intended `releaseBundleId`, and state the rollback signal and owner.
11. After triggering, read release bundle and execution task status, logs, and artifacts when those tools are available.
12. Return a compact handoff with status, IDs, links if present, and the next safe manual step.

## Examples

### Input Example

User asks: "Build the payments API from branch `release/2026-06-09` into staging and show me the task status."

### Expected Tool Calls

1. `delivery.applications.list` with a search term such as `payments`.
2. `delivery.applications.detail` for the selected `applicationId`.
3. `delivery.application_environments.list` to select the staging binding.
4. `delivery.build_sources.list` to select the build source.
5. `delivery.release.plan` with `action=build`, the selected application environment, branch or commit, and a non-secret reason.
6. After human confirmation, the platform creates/confirms the `DeliveryPlan` and only then invokes execution.
7. `delivery.execution_tasks.list` and `delivery.execution_logs.list` to report task status and redacted log evidence.

## Permission Boundaries

- Requires Gateway-visible delivery capabilities for the current identity and the `businessLine`, `application`, and `environment` scopes.
- Uses only non-secret application metadata and release identifiers in arguments.
- Treats `delivery.release.plan` as preview output only; execution requires a human-confirmed `DeliveryPlan`.
- Treats approval-required responses from `delivery.actions.trigger` as the terminal handoff.
- Treats `DeliveryDraft` confirmation as a separate human-approved mutation, never as part of repository analysis or draft generation.

## Forbidden Actions

- Do not pass access token, refresh token, kubeconfig, password, registry credential, environment variable, or runner secret values into Gateway tools.
- Do not bypass `delivery.actions.trigger` by calling CI, Docker, Kubernetes, PostgreSQL, or runners directly.
- Do not deploy to production, verify, or roll back unless the user explicitly names the target and intent.
- Do not create applications, services, environment bindings, or file changes directly from AI onboarding output; route them through `DeliveryDraft` preview and confirmation.
- Do not trigger delivery directly from AI release planning output; route it through `DeliveryPlan` preview and confirmation.

## Guardrails

- Do not include access tokens, refresh tokens, kubeconfig, registry credentials, environment variables, or runner secrets in tool arguments or output.
- Do not trigger production deploys unless the user explicitly names the production environment and confirms intent.
- Do not trigger rollback without explicit user intent, a target application environment, and a release bundle or rollback context.
- If Gateway reports approval is required, stop at the approval handoff and do not retry as a different action.
- If a capability is missing, explain the missing permission or scope instead of inventing a workaround.
