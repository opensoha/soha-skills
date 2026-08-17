---
id: k8s-resource-provisioner
name: K8s Resource Provisioner
version: 0.1.0
category: platform
description: Kubernetes workload snapshot generation plus approval-bound manifest preflight and creation for scoped environments.
capabilityRefs:
  - k8s.workloads.snapshot.generate
  - k8s.resources.create.preflight
  - k8s.resources.create.trigger
requiredScopes:
  - cluster
  - namespace
---

# K8s Resource Provisioner

Use this skill to generate workload snapshots, then validate and create bounded Kubernetes resources through Soha.

## Operating Contract

- Discover the capabilities required by the requested workflow from the live Gateway manifest before use.
- Treat snapshot generation as read-only manifest preparation; it never creates or synchronizes a resource.
- Always preflight the exact content before requesting creation.
- Reuse one stable idempotency key when retrying the same creation request.
- When external credentials are required, attach canonical references through `_sohaSecretRefs`; keep them outside Kubernetes manifests and business input.

## Workflow

1. Confirm the target cluster and namespace.
2. When deriving a Job, CronJob, or image-following WorkloadCronJob, call `k8s.workloads.snapshot.generate` with one Deployment, StatefulSet, or DaemonSet source and review the generated manifest.
3. Select only secrets bound to the capability and target cluster or namespace, then call `k8s.resources.create.preflight` with the final credential-free manifest.
4. Stop on any authorization, capability, dry-run, or scope error.
5. Present the plan and obtain the required human approval.
6. Call `k8s.resources.create.trigger` with the same content, secret references, and a stable idempotency key.
7. Report the operation id, content hash, and per-document result.

## Examples

### Input Example

Generate a CronJob from Deployment `reports` in namespace `demo` on cluster `lab`, then create it.

### Expected Tool Calls

1. `k8s.workloads.snapshot.generate` for Deployment `reports` and the target CronJob.
2. `k8s.resources.create.preflight` for cluster `lab` and namespace `demo`.
3. `k8s.resources.create.trigger` only after the preflight is ready and approval is granted.

## Permission Boundaries

- Snapshot generation requires exact source workload `view` and target Job, CronJob, or custom resource `create` permissions.
- Preflight and execution require scoped cluster and namespace access plus `platform.resource-creation.use`.
- Every manifest still requires the exact resource-kind `create` permission for its target namespace or cluster scope.
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
