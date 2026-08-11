---
id: virtualization-operator
name: Virtualization Operator
version: 0.1.0
category: platform
description: Approval-bound virtual machine planning, creation, and typed lifecycle operations through Soha.
capabilityRefs:
  - virtualization.vms.create.plan
  - virtualization.vms.create.trigger
  - virtualization.vms.action.trigger
requiredScopes:
  - virtualizationConnection
  - vm
---

# Virtualization Operator

Use this skill to plan and operate virtual machines through Soha provider adapters.

The MCP surface is intentionally limited to create planning, create execution, and typed VM actions. Use the Soha workbench or public HTTP API for inventory and detail reads.

## Operating Contract

- Discover all VM tools from the live Gateway manifest before use.
- Confirm the selected connection is enabled and direct. Agent-connected KubeVirt virtualization is not supported.
- Use only actions returned by the VM's live `allowedActions`; do not assume provider parity. KubeVirt currently advertises CPU and memory resize only.
- Plan every VM create request before execution.
- Use typed lifecycle actions and stable idempotency keys only.
- When provider or bootstrap credentials are required, attach canonical references through `_sohaSecretRefs`; keep them outside cloud-init and business input.

## Workflow

1. Confirm the virtualization connection, image, flavor, VM name, and requested resources.
2. Select only secrets bound to the capability and target connection, then call `virtualization.vms.create.plan` and review warnings and redaction indicators.
3. Present the plan and obtain required approval.
4. Call `virtualization.vms.create.trigger` with the approved input, the same secret references, and a stable idempotency key.
5. Use `virtualization.vms.action.trigger` only for a named typed action on a known VM id.

## Examples

### Input Example

Create a small VM named `demo-api` from an approved image and flavor.

### Expected Tool Calls

1. `virtualization.vms.create.plan` for the selected connection.
2. `virtualization.vms.create.trigger` only after approval.

## Permission Boundaries

- Requires explicit virtualization connection and VM scope.
- Image, flavor, provider, policy, and approval checks remain server-side.
- PVE and KubeVirt availability depends on the selected live connection and its reported capabilities; this skill does not assert lab or provider readiness.
- Secret-backed operations additionally require `secret.use`; the server enforces secret scope, bindings, approval, and audit.

## Forbidden Actions

- Do not request provider passwords, API tokens, private keys, credentials, or console secrets.
- Do not run provider CLI, shell, SSH, raw hypervisor commands, or untyped VM actions.

## Guardrails

- Keep cloud-init credentials and secret material out of plans, logs, and chat output.
- Pass references only through `_sohaSecretRefs`; never pass, resolve, log, or return secret values.
- Stop if the plan changes before execution and request a new approval.
- Reuse an idempotency key only for an identical approved request.
