---
id: k8s-resource-provisioner
name: K8s Resource Provisioner
version: 0.1.0
category: platform
description: Approval-bound Kubernetes manifest preflight and creation for scoped demo environments.
capabilityRefs:
  - k8s.resources.create.preflight
  - k8s.resources.create.trigger
requiredScopes:
  - cluster
  - namespace
---

# K8s Resource Provisioner

Use this skill to validate and create bounded Kubernetes demo resources through Soha.

## Operating Contract

- Discover both capabilities from the live Gateway manifest before use.
- Always preflight the exact content before requesting creation.
- Reuse one stable idempotency key when retrying the same creation request.
- When external credentials are required, attach canonical references through `_sohaSecretRefs`; keep them outside Kubernetes manifests and business input.

## Workflow

1. Confirm the target cluster and namespace.
2. Select only secrets bound to the capability and target cluster or namespace, then call `k8s.resources.create.preflight` with the final credential-free manifest.
3. Stop on any authorization, capability, dry-run, or scope error.
4. Present the plan and obtain the required human approval.
5. Call `k8s.resources.create.trigger` with the same content, secret references, and a stable idempotency key.
6. Report the operation id, content hash, and per-document result.

## Examples

### Input Example

Create a small Deployment and Service in namespace `demo` on cluster `lab`.

### Expected Tool Calls

1. `k8s.resources.create.preflight` for cluster `lab` and namespace `demo`.
2. `k8s.resources.create.trigger` only after the preflight is ready and approval is granted.

## Permission Boundaries

- Requires scoped cluster and namespace access plus `platform.resource.create` for execution.
- The Gateway and resource service enforce resource-kind, namespace, and high-risk permissions.
- Secret-backed operations additionally require `secret.use`; the server enforces secret scope, bindings, approval, and audit.

## Forbidden Actions

- Do not request kubeconfig, access token, password, private key, credential, or Secret payloads.
- Do not run `kubectl`, shell, exec, port-forward, delete, patch, or arbitrary commands.

## Guardrails

- Never place credentials or secret values in manifests, logs, plans, or chat output.
- Pass references only through `_sohaSecretRefs`; never pass, resolve, log, or return secret values.
- Treat preflight success as evidence, not authorization to skip approval.
- Do not change the content or idempotency key between approved retries.
