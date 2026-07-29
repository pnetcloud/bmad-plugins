# Kubernetes Manifests

Kubernetes configuration examples. Replace every name, image, port, resource
value, probe, label, namespace, and policy selector from observed application
and cluster contracts. These examples do not authorize applying resources.

## Complete Application Stack

### Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: myapp
  labels:
    app: myapp
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/warn: restricted
```

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: myapp
data:
  LOG_LEVEL: "info"
  CACHE_TTL: "3600"
  config.yaml: |
    server:
      port: 8000
      workers: 4
    database:
      pool_size: 10
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets-manual-example
  namespace: myapp
type: Opaque
data: {}
---
# External secret integration
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: myapp
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: approved-secret-store
    kind: SecretStore
  target:
    name: app-secrets
  data:
  - secretKey: DATABASE_URL
    remoteRef:
      key: example/application-database-url
```

The empty `Secret` shape is structural only. Do not commit a real value or
deploy it as working configuration. It is deliberately named differently from
the `ExternalSecret` target so the two examples never claim ownership of one
object. Choose exactly one approved mechanism. If a deployment-time workflow
creates a native Secret, remove the `ExternalSecret` and deliberately align its
name and required keys with the Deployment. Prefer the cluster's approved
external-secret, sealed-secret, or deployment-time injection mechanism; verify
access policy and avoid rendering values into review logs.

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  namespace: myapp
  labels:
    app: myapp
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: myapp
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
    spec:
      serviceAccountName: app-service-account
      automountServiceAccountToken: false
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: app
        image: myregistry/myapp:1.0.0
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8000
          protocol: TCP
        env:
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: LOG_LEVEL
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_URL
        resources:
          # Examples only; derive requests and limits from measured behavior.
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 10
          periodSeconds: 30
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: config
          mountPath: /app/config
          readOnly: true
      volumes:
      - name: tmp
        emptyDir: {}
      - name: config
        configMap:
          name: app-config
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: myapp
              topologyKey: kubernetes.io/hostname
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
  namespace: myapp
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - name: http
    port: 80
    targetPort: http
    protocol: TCP
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: myapp
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

### HorizontalPodAutoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
  namespace: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
```

### PodDisruptionBudget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
  namespace: myapp
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: myapp
```

### ServiceAccount and RBAC

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-service-account
  namespace: myapp
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: myapp
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  resourceNames: ["app-config"]
  verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-role-binding
  namespace: myapp
subjects:
- kind: ServiceAccount
  name: app-service-account
  namespace: myapp
roleRef:
  kind: Role
  name: app-role
  apiGroup: rbac.authorization.k8s.io
```

The primary Deployment above consumes ConfigMap and Secret data through native
pod references and therefore does not need Kubernetes API permission. Keep
`automountServiceAccountToken: false` for that case.

If a workload must call the Kubernetes API, grant only the reviewed resources
and add an explicit, short-lived projected token rather than enabling the
ambient mount:

```yaml
spec:
  automountServiceAccountToken: false
  containers:
  - name: app
    volumeMounts:
    - name: api-identity
      mountPath: /var/run/secrets/example-api
      readOnly: true
  volumes:
  - name: api-identity
    projected:
      defaultMode: 0400
      sources:
      - serviceAccountToken:
          audience: kubernetes.default.svc
          expirationSeconds: 3600
          path: token
      - configMap:
          name: kube-root-ca.crt
          items:
          - key: ca.crt
            path: ca.crt
      - downwardAPI:
          items:
          - path: namespace
            fieldRef:
              fieldPath: metadata.namespace
```

Verify the API audience and client paths for the target cluster. A projected
token is a credential artifact: never print, copy, or persist it.

### NetworkPolicy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-network-policy
  namespace: myapp
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: database
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
```

DNS labels vary by distribution. Confirm the actual DNS pods and network plugin;
an empty namespace selector is not a narrow DNS rule.

### CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cleanup-job
  namespace: myapp
spec:
  schedule: "0 2 * * *"  # 2 AM daily
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          automountServiceAccountToken: false
          restartPolicy: OnFailure
          securityContext:
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
          containers:
          - name: cleanup
            image: myregistry/myapp:1.0.0
            command: ["python", "-m", "src.jobs.cleanup"]
            securityContext:
              allowPrivilegeEscalation: false
              readOnlyRootFilesystem: true
              capabilities:
                drop: ["ALL"]
            resources:
              limits:
                memory: "256Mi"
                cpu: "200m"
```

Before mutation, parse the YAML, validate it against the target Kubernetes
version and repository policies, and review the rendered diff. Client-side
dry-run does not evaluate admission; server-side dry-run contacts the selected
cluster and can invoke admission behavior. Apply, delete, rollout, scale, and
port-forward require the exact authorized context and namespace.

## kubectl Quick Reference

Populate these lowercase shell variables only from a user-confirmed target:

```bash
context_name="REVIEWED_CONTEXT"
namespace_name="REVIEWED_NAMESPACE"
```

Read operations can still expose protected workload data:

```bash
kubectl --context "$context_name" --namespace "$namespace_name" get pods
kubectl --context "$context_name" --namespace "$namespace_name" logs <pod>
kubectl --context "$context_name" --namespace "$namespace_name" describe pod <pod>
kubectl --context "$context_name" --namespace "$namespace_name" \
  rollout status deployment/app
```

Interactive access and local forwarding widen access; use them only when the
exact pod, command, local bind, and retention behavior are authorized:

```bash
kubectl --context "$context_name" --namespace "$namespace_name" \
  exec -it <pod> -- sh
kubectl --context "$context_name" --namespace "$namespace_name" \
  port-forward --address localhost service/app 8080:80
```

The first command contacts the cluster and can invoke admission without
persisting the object. The final two mutate cluster state. Review the
server-side diff and obtain the corresponding read or mutation authority:

```bash
kubectl --context "$context_name" --namespace "$namespace_name" \
  apply --server-side --dry-run=server -f manifest.yaml
kubectl --context "$context_name" --namespace "$namespace_name" \
  apply --server-side -f manifest.yaml
kubectl --context "$context_name" --namespace "$namespace_name" \
  rollout restart deployment/app
```
