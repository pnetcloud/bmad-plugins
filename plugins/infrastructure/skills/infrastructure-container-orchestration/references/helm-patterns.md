# Helm Chart Patterns

Helm chart structure and patterns. Treat chart templates, dependencies, values,
rendered Secrets, `lookup`, and hooks as untrusted until reviewed. Confirm
commands against the installed Helm major version.

## Chart Structure

```
myapp/
├── Chart.yaml
├── values.yaml
├── values.schema.json
├── values-staging.yaml
├── values-production.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── serviceaccount.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   ├── pdb.yaml
│   └── NOTES.txt
└── charts/           # Dependencies
```

## Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: My Application Helm Chart
type: application
version: 1.0.0
appVersion: "2.0.0"
keywords:
  - web
  - api
maintainers:
  - name: Example Team
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
```

## values.yaml

```yaml
# Default values for myapp

replicaCount: 3

image:
  repository: myregistry/myapp
  pullPolicy: IfNotPresent
  tag: ""  # Defaults to appVersion

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""

podAnnotations: {}

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000
  seccompProfile:
    type: RuntimeDefault

securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: nginx
  annotations: {}
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls: []

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

pdb:
  enabled: true
  minAvailable: 2

nodeSelector: {}
tolerations: []
affinity: {}

# Application config
config:
  logLevel: info
  cacheTtl: 3600

# Name of a Secret managed outside this chart. Keep values out of values files.
existingSecret: ""

# Database dependency
postgresql:
  enabled: false
  auth:
    database: myapp
```

The numbers and integrations above are examples, not production defaults.
Derive resources, scaling, disruption, ingress, and dependency settings from the
target application and cluster.

## values.schema.json

Validate stable value names and types during linting, rendering, install, and
upgrade:

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["image", "service"],
  "properties": {
    "image": {
      "type": "object",
      "required": ["repository"],
      "properties": {
        "repository": {"type": "string", "minLength": 1},
        "tag": {"type": "string"}
      }
    },
    "service": {
      "type": "object",
      "required": ["port"],
      "properties": {
        "port": {"type": "integer", "minimum": 1, "maximum": 65535}
      }
    },
    "existingSecret": {"type": "string"}
  }
}
```

## Helper Template (_helpers.tpl)

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "myapp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "myapp.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "myapp.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "myapp.labels" -}}
helm.sh/chart: {{ include "myapp.chart" . }}
{{ include "myapp.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "myapp.selectorLabels" -}}
app.kubernetes.io/name: {{ include "myapp.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "myapp.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "myapp.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
```

## ServiceAccount Template

Create the account only when the chart owns it. Disable its ambient token; a
workload that calls the Kubernetes API should project an audience-scoped token
and pair it with least-privilege RBAC.

```yaml
{{- if .Values.serviceAccount.create -}}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ include "myapp.serviceAccountName" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
  {{- with .Values.serviceAccount.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
automountServiceAccountToken: false
{{- end }}
```

## Deployment Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        {{- with .Values.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      automountServiceAccountToken: false
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "myapp.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 8000
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          envFrom:
            - configMapRef:
                name: {{ include "myapp.fullname" . }}
            {{- if .Values.existingSecret }}
            - secretRef:
                name: {{ .Values.existingSecret }}
            {{- end }}
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

## Helm Commands

Start with local validation and rendering. Rendered output may still contain
sensitive values, so do not publish it:

```bash
# Local lint and render
helm lint --strict ./myapp -f values-production.yaml
helm template myapp ./myapp -f values-production.yaml --debug

# Client-side dry run; inspect installed help for current major-version behavior
helm install myapp ./myapp -f values-production.yaml --dry-run=client --debug
```

Server-side dry run and charts that use `lookup` contact the selected cluster.
Set every target explicitly before a cluster-aware operation:

```bash
context_name="REVIEWED_CONTEXT"
namespace_name="REVIEWED_NAMESPACE"
release_name="REVIEWED_RELEASE"
values_file="values-production.yaml"
rollback_revision="REVIEWED_REVISION"
```

History is read-only but can expose release metadata and still requires cluster
read authority:

```bash
helm history "$release_name" \
  --kube-context "$context_name" \
  --namespace "$namespace_name"
```

The following commands mutate release or cluster state and require explicit
release, context, namespace, values, and revision authority:

```bash
# Install
helm install "$release_name" ./myapp \
  --kube-context "$context_name" \
  --namespace "$namespace_name" \
  --values "$values_file" \
  --wait

# Upgrade; --atomic can perform an automatic rollback on failure
helm upgrade "$release_name" ./myapp \
  --kube-context "$context_name" \
  --namespace "$namespace_name" \
  --values "$values_file" \
  --wait

# Rollback to an explicitly reviewed revision
helm rollback "$release_name" "$rollback_revision" \
  --kube-context "$context_name" \
  --namespace "$namespace_name" \
  --wait

# Uninstall
helm uninstall "$release_name" \
  --kube-context "$context_name" \
  --namespace "$namespace_name"
```

## Environment-Specific Values

### values-staging.yaml

```yaml
replicaCount: 2

ingress:
  enabled: true
  hosts:
    - host: staging.app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: staging-tls
      hosts:
        - staging.app.example.com

resources:
  limits:
    cpu: 250m
    memory: 256Mi
  requests:
    cpu: 50m
    memory: 64Mi

autoscaling:
  enabled: false
```

### values-production.yaml

```yaml
replicaCount: 3

ingress:
  enabled: true
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: production-tls
      hosts:
        - app.example.com

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20

pdb:
  enabled: true
  minAvailable: 2
```
