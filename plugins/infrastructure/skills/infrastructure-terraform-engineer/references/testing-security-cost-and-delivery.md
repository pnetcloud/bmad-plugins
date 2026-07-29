# Testing, Security, Cost, and Delivery

Use this reference for validation, CI/CD, governance, cost, compliance, or
operational readiness.

## Contents

- Test and validation matrix
- Security and compliance
- Cost and resource governance
- Environments and CI/CD
- Enterprise governance and operations
- Documentation and handoffs

## Test and Validation Matrix

| Layer | Evidence |
| --- | --- |
| Format/static | repository formatter, syntax, validation, lint, docs consistency |
| Unit | pure expression, input, output, condition, and invariant behavior |
| Expression/module | inputs, outputs, conditions, keys, invariants, failure cases |
| Mocked or plan test | resource graph and assertions without assumed live effects |
| Provider integration | isolated target, real API behavior, cleanup/reconciliation |
| Policy/compliance | exact rule/version/scope, exceptions, false-positive review |
| Security | exposed surfaces, IAM, secrets/state, encryption, logging, dependencies |
| Cost | estimator scope, unknowns, quantity/rate assumptions, recurring/one-time cost |
| Migration/state | import, move, removed resource, backend/state transition, full plan |
| Performance/capacity | provider/API limits, graph scale, duration, concurrency, quotas |
| Recovery | interrupted/partial apply, lock, state backup/restore, remote reconciliation |
| End-to-end | approved plan, exact apply target, observation, drift, and recovery evidence |

`terraform validate` checks configuration consistency, not provider-side policy
or a safe deployment. A clean plan, policy scan, security scan, or cost
estimate covers only its declared inputs and rules.

Terraform test files can use plan or apply modes, mocks, overrides, and helper
modules depending on the selected version. Inspect every run before execution.
Real apply-mode tests can create costly resources and failed cleanup leaves
residual infrastructure; use dedicated purgeable targets and an owner.

## Security and Compliance

- Threat-model state, plan artifacts, provider/plugin supply chain, execution
  identity, CI logs, remote backends, exposed network paths, data, and resource
  deletion—not only HCL attributes.
- Derive least privilege from planned actions and operational needs. Avoid
  copying wildcard example policies; plan and refresh may require reads, while
  apply requires distinct mutation authority.
- Keep credentials out of HCL, variable defaults, committed variable files,
  backend configuration, command arguments, generated docs, logs, plans, and
  test fixtures. Prefer bounded dynamic credentials where supported.
- Validate network exposure from effective ingress/egress, routes, identities,
  load balancers, DNS, and service controls. A single resource flag is not a
  complete boundary.
- Define encryption requirements for transport, remote storage, state, plans,
  logs, backups, and managed resources, including key ownership and recovery.
- Map policy/compliance findings to the exact current rule and applicability.
  Record exception owner, rationale, scope, expiry, compensating controls, and
  retest. A benchmark is guidance, not universal compliance.
- Preserve audit evidence without storing sensitive plan/state contents longer
  than required.

## Cost and Resource Governance

- Estimate from the reviewed plan, quantities, regions, pricing date/source,
  discounts/commitments, usage assumptions, data transfer, storage growth,
  logs, backups, support, and dependent services.
- Report known, estimated, unknown, and excluded cost separately. Do not claim
  savings from static HCL alone.
- Use required tags or labels from repository policy. Validate propagation and
  resources that do not support them rather than forcing a universal map.
- Define budget/alert owner, scope, currency, period, threshold, delay, and
  response. Alerts do not enforce a hard spending cap.
- Base optimization, waste, chargeback, or showback recommendations on observed
  ownership and usage evidence; preserve reliability and commitments.

## Environments and CI/CD

- Isolate environments through an explicit combination of state, credentials,
  account/project, network, policy, and approval boundaries. DRY configuration
  must not hide environment-specific risk.
- Promote reviewed module/configuration versions and inputs; do not assume a
  plan is portable between states or environments.
- Serialize writers per state. Bind plan artifacts to source revision,
  dependency lock, variables, target, identity, and approval; protect them as
  sensitive and expire them.
- Separate speculative pull-request plans from final executable plans. Re-plan
  when state, configuration, dependencies, credentials, or material external
  facts changed.
- Gate apply by exact environment risk. Automated approval may be appropriate
  for bounded low-risk targets; “human approval always” is not a substitute for
  policy, tests, or plan integrity.
- Generate documentation and changelogs from reviewed source but fail when
  generation drifts. Do not silently rewrite unrelated files.
- Define rollback/forward-repair, incident response, partial apply, cleanup,
  drift observation, and escalation before production mutation.

## Enterprise Governance and Operations

Choose repository layout, registries, policy engines, role-based access (RBAC),
change-management evidence, audit retention, and separation of duties from
organization size, risk, ownership, and tooling—not an “enterprise” template.

Define:

- module/provider/source allowlists and provenance;
- owner and reviewer boundaries for code, state, plans, and apply;
- break-glass and force-unlock controls;
- version/upgrade and deprecation policy;
- drift detection cadence, identity, alert routing, and remediation authority;
- incident, recovery, knowledge-transfer, and training ownership.

Drift detection is a remote read workflow with credentials, rate limits, locks,
cost, sensitive output, and false-positive handling. It does not authorize
automatic reconciliation.

## Documentation and Handoffs

Keep module usage, inputs/outputs, resources, assumptions, state/backend,
provider/version, environment, plan/apply, security/cost, incident, and
recovery documentation close to its authoritative source.

Exchange:

- architecture, network, database, Kubernetes, and platform invariants with
  their respective owners;
- module/state/plan/pipeline contracts and actual run evidence with operations
  and SRE owners;
- threat, IAM, network, encryption, policy, and exception evidence with
  security owners;
- estimate assumptions, tags, budgets, usage, and attribution evidence with
  cost owners;
- test scope, fixtures, target isolation, results, and residual cleanup with
  QA/review owners.

Do not turn a handoff into a claim that the receiving owner approved or ran it.
