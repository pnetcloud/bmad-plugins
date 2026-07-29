# Landing Zones, Security, Networking, and Governance

Use for organization foundations, accounts, identity, network, policy, compliance, and shared platform boundaries.

## Contents

- [Landing-zone contract](#landing-zone-contract)
- [Identity and security](#identity-and-security)
- [Network architecture](#network-architecture)
- [Governance and compliance](#governance-and-compliance)
- [Validation](#validation)

## Landing-zone contract

A landing zone is a governed foundation, not a universal account template. Establish:

- organization, tenant, account, subscription, and project hierarchy;
- environment and workload isolation, ownership, quotas, and lifecycle;
- human, workload, automation, break-glass, and provider support identities;
- policy inheritance, exceptions, audit, and change authority;
- network, DNS, ingress, egress, private connectivity, and shared services;
- logging, detection, key management, backup, recovery, cost allocation, and tagging;
- bootstrap, IaC state, drift, upgrade, and decommission ownership.

Guardrails need a tested permitted path, denial evidence, exception lifecycle, and recovery. Centralization should not create an unowned bottleneck or a single high-privilege deployment identity.

## Identity and security

Apply zero-trust principles as explicit verification and least privilege, not as a completion label. Map principals to actions, resources, conditions, sessions, and trust sources. Prefer federation and bounded temporary credentials; avoid routine root or owner use, broad wildcards, shared identities, and long-lived keys.

Review privilege escalation through policy delegation, role assumption, pass-role or impersonation, automation, metadata services, secrets, key management, resource policies, network controls, and organization administration. Break-glass access needs strong authentication, limited scope and duration, monitoring, audit, recovery, and review.

Classify data and define encryption in transit and at rest, key ownership, separation of duties, rotation, revocation, availability, backup, deletion, and legal retention. Encryption does not replace authorization, minimization, or application-level controls.

Threat modeling covers actors, assets, trust boundaries, entry points, abuse paths, supply chain, detection, response, and residual risk. Provider posture or benchmark tools are bounded inputs; scanners do not prove application security or compliance.

## Network architecture

Derive VPC/VNet, subnet, route, firewall/security-group, load balancer, CDN, DNS, VPN, and private-link choices from required flows and failure behavior.

- use explicit ingress and egress paths, identities, protocols, destinations, ownership, and logging;
- model address capacity, overlap, IPv4/IPv6, routing convergence, asymmetric paths, NAT, quotas, and appliances;
- verify DNS delegation, split horizon, TTL, negative caching, DNSSEC where applicable, ownership, failover, and recovery;
- define TLS certificate and key lifecycle, endpoint serving, client trust, overlap, revocation, and expiry;
- validate direct-connect/private-circuit redundancy including customer, provider, device, facility, route, and control-plane failure;
- treat CDN and edge caching as data distribution with freshness, invalidation, privacy, origin protection, and failure contracts.

Network changes, DNS, certificates, routes, security groups, and traffic shifts are remote mutations requiring exact authority and staged observation.

## Governance and compliance

Translate laws, contracts, policies, and data-residency requirements into scoped controls and evidence with responsible legal, privacy, security, and audit owners. Architecture can support compliance; the skill must not independently certify it.

Define policy source, revision, scope, enforcement point, exception owner, reason, compensating control, expiry, and review. Compliance automation collects or enforces bounded evidence; it does not turn a passing scan into approval.

Tagging and metadata need an explicit decision consumer, controlled vocabulary, ownership, validation, privacy review, and reconciliation. Do not encode sensitive customer, incident, or personal data in globally visible resource names or tags.

Shared responsibility varies by provider, service, configuration, and workload. Record provider, platform, workload, data, security, finance, and operations ownership for every control rather than copying a generic matrix.

## Validation

Use source inspection, policy tests with allow and deny cases, IaC plan/change-set review, identity simulation or authorization tests, isolated deployment, network reachability and denial tests, audit and detection evidence, recovery exercises, and staged workload observation.

Keep provider, service, region, API and policy versions, identities, scopes, collection times, suppressions, and exceptions with results. A successful control-plane request is not proof of data-plane reachability, user authorization, workload health, or compliance.
