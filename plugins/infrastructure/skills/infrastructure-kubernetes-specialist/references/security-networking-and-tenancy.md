# Security, Networking, Service Mesh, and Tenancy

Use this reference when Kubernetes identity, authorization, workload hardening, policy, networking, service mesh, or multi-tenancy is in scope.

## Contents

- [Threat and authority boundary](#threat-and-authority-boundary)
- [Identity, RBAC, and Secrets](#identity-rbac-and-secrets)
- [Pod and admission security](#pod-and-admission-security)
- [Networking and DNS](#networking-and-dns)
- [Service mesh](#service-mesh)
- [Multi-tenancy](#multi-tenancy)
- [Security validation](#security-validation)

## Threat and authority boundary

Record the protected assets, tenant and workload trust levels, human and workload identities, ingress and egress paths, cluster-scoped control surfaces, node and storage sharing, and plausible privilege-escalation paths. Do not convert a checklist or scanner result into a blanket “secure” or “compliant” claim.

Even read-only Kubernetes permissions can disclose Secrets, ConfigMaps, logs, exec output, environment values, Pod specifications, node topology, image sources, and tenant metadata. Use the least data-bearing query, restrict namespace and selectors, avoid broad list/watch access, and redact values from evidence.

## Identity, RBAC, and Secrets

- Prefer namespaced Roles and RoleBindings and the smallest verbs, API groups, resources, names, and namespaces that implement the task.
- Avoid wildcards, routine `cluster-admin`, `system:masters`, broad impersonation, and permissions that indirectly create privileged workloads or bind stronger roles.
- Use a dedicated service account per workload where identity is needed. Disable automatic token mounting when API access is not required.
- Prefer bounded, audience-specific, short-lived credentials and workload identity mechanisms. Do not create or copy long-lived tokens for convenience.
- Review privilege through Secrets, Pods, workloads, admission, nodes, persistent volumes, certificates, token requests, `escalate`, `bind`, `impersonate`, and controller-managed resources.
- Treat Secret values as confidential even when base64-encoded. Never commit plaintext Secret manifests or echo decoded values into reports. Bound encryption-at-rest, external secret, rotation, revocation, propagation, and failure behavior to the actual platform.

RBAC modification requires explicit authority and a before/after authorization proof for the intended identity. A successful `can-i` query is scoped evidence, not proof that every privilege-escalation path is absent.

## Pod and admission security

Select the applicable Pod Security Standards level and enforcement mode for the workload and version. Evaluate:

- non-root execution and user/group ownership;
- privilege escalation, Linux capabilities, seccomp, host namespaces, host paths, devices, and privileged mode;
- read-only root filesystem and required writable paths;
- service-account tokens, projected credentials, Secret and ConfigMap mounts;
- image identity, provenance, supported base, vulnerability evidence, and registry trust;
- runtime class, sandboxing, node isolation, and exposure to less-trusted workloads.

PodSecurityPolicy was deprecated in Kubernetes v1.21 and removed in v1.25. Preserve it only for historical audit and migration. For supported clusters, evaluate Pod Security Admission and, when the requirement exceeds predefined standards, an admission policy or external controller with explicit ownership, availability, audit/enforce rollout, failure policy, exception lifecycle, and recovery.

OPA or another policy engine is not self-validating. Pin policy and bundle identity, test allow and deny cases, protect distribution, bound external data, and define failure behavior. Exceptions need an owner, exact scope, reason, expiry, and review.

Admission webhooks sit on the API path. Verify scope, side effects, match conditions, timeouts, failure policy, reinvocation, certificate lifecycle, HA, version compatibility, and behavior when unavailable. Stage enforcement through representative audit or warning evidence before blocking production where possible.

## Networking and DNS

Establish the CNI, NetworkPolicy support, data paths, address families, service implementation, ingress or Gateway controller, load balancer, DNS, egress, and multi-cluster mechanism. A NetworkPolicy object has no effect if the CNI does not implement it.

For policies:

1. map required ingress, egress, DNS, control-plane, metadata, storage, observability, and external dependency flows;
2. use trusted namespace and Pod labels and account for their ownership;
3. stage default-deny with explicit required allowances;
4. test allowed and denied traffic from representative identities;
5. observe drops without collecting sensitive payloads;
6. maintain a bounded break-glass and recovery path.

Services and ingress require selector and endpoint correctness, port mapping, readiness, source IP and proxy semantics, TLS ownership, client trust, timeouts, retries, connection draining, and controller-specific behavior. DNS validation includes namespace search behavior, caching, negative responses, resolver limits, and failure impact.

For multi-cluster networking, make service identity, discovery freshness, routing, encryption, failure isolation, split-brain behavior, data locality, and ownership explicit. Do not equate connectivity with continuity.

## Service mesh

Adopt Istio, Linkerd, or another mesh only for an evidenced traffic, identity, security, or observability need that justifies its latency, resource, upgrade, failure, and operator cost. Define:

- workload identity and trust-domain boundaries;
- certificate issuance, rotation, overlap, revocation, and unavailable-control-plane behavior;
- traffic ownership, retries, timeouts, circuit breaking, outlier handling, and retry amplification;
- sidecar or ambient data-path lifecycle and application probe behavior;
- telemetry privacy, cardinality, sampling, retention, and access;
- staged policy and version upgrades plus exit or bypass strategy.

Traffic shifting and A/B tests need immutable workload identity, cohort selection, statistical and product ownership, capacity, observation, abort, and recovery. Mesh configuration acceptance is not proof that application behavior is safe.

## Multi-tenancy

Choose the isolation model from threat and operating requirements: namespaces in a shared control plane, virtualized control planes, or dedicated clusters. Namespaces scope many objects but are not a complete security boundary.

Evaluate:

- RBAC and admission for tenant and platform identities;
- default and required network flows plus cross-namespace DNS;
- ResourceQuota, LimitRange, priority, API fairness, and noisy-neighbor risks;
- node, kernel, runtime, device, storage, and persistent-volume isolation;
- cluster-scoped CRDs, webhooks, StorageClasses, controllers, and policy ownership;
- audit access, tenant metadata, cost allocation, and retention;
- tenant onboarding, offboarding, deletion, backup, restore, and residual data;
- platform administration and break-glass paths.

Stronger workload distrust may require node isolation, sandboxing, virtual control planes, or dedicated clusters. State the residual shared-control-plane, node, network, and storage risks.

## Security validation

Use complementary evidence:

- source and rendered-manifest inspection;
- version-aware schema and policy tests with positive and negative cases;
- image, dependency, and provenance evidence;
- authorization tests for exact identities;
- admission dry runs or isolated applies;
- representative network allow/deny tests;
- runtime security, audit, event, and controller observations;
- exception and residual-risk review.

Keep tool revisions, policy revisions, scope, suppressions, and collection time. Scanners and benchmarks are bounded inputs; they do not independently approve architecture, tenant isolation, runtime behavior, or compliance.
