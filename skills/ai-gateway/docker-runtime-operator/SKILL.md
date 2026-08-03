---
id: docker-runtime-operator
name: Docker Runtime Operator
version: 0.1.0
category: platform
description: Approval-bound Docker host, Compose project, and service operations through Soha.
capabilityRefs:
  - docker.hosts.quick_create.plan
  - docker.hosts.quick_create.trigger
  - docker.projects.deploy.plan
  - docker.projects.deploy.trigger
  - docker.services.action.trigger
requiredScopes:
  - virtualizationConnection
  - dockerHost
  - dockerProject
  - dockerService
---

# Docker Runtime Operator

Use this skill to provision Docker hosts and operate existing Compose projects through Soha.

## Operating Contract

- Discover every tool from the live Gateway manifest before use.
- Plan host creation and project deployment before requesting execution.
- Use only typed actions and stable idempotency keys.
- When credentials are required, attach canonical references through `_sohaSecretRefs`; keep them outside Compose content and business input.

## Workflow

1. Confirm the virtualization connection, Docker host, project, and service scope.
2. Select only secrets bound to the capability and target connection or project, then call the matching `.plan` tool.
3. Present changes, warnings, and approval requirements.
4. Call the matching `.trigger` tool only after approval, with the same secret references used by the plan.
5. Track the returned durable operation id instead of repeating execution.

## Examples

### Input Example

Deploy project `demo-api` on an existing Docker host.

### Expected Tool Calls

1. `docker.projects.deploy.plan` with the scoped project id.
2. `docker.projects.deploy.trigger` with the approved input and stable idempotency key.

## Permission Boundaries

- Host provisioning requires both Docker host and virtualization VM permissions.
- Project and service actions remain bound to the selected Docker host and object ids.
- Secret-backed operations additionally require `secret.use`; the server enforces secret scope, bindings, approval, and audit.

## Forbidden Actions

- Do not request SSH keys, passwords, tokens, secret material, credentials, or raw daemon access.
- Do not run shell commands or send untyped Docker, Compose, or system commands.

## Guardrails

- Keep secrets out of Compose content, environment values, plans, logs, and chat output.
- Pass references only through `_sohaSecretRefs`; never pass, resolve, log, or return secret values.
- Stop when a required capability is absent or an operation is pending approval.
- Reuse the operation id for status tracking and the idempotency key only for identical retries.
