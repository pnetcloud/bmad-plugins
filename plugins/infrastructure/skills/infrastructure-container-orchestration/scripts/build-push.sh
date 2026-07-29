#!/usr/bin/env bash
# Build an explicitly named image and optionally push that exact reference.

set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  build-push.sh --image NAME --tag TAG [options]

Required:
  --image NAME          Repository-local image name, for example service-api
  --tag TAG             Immutable release or review tag; "latest" is rejected

Options:
  --registry HOST       Registry host or host/path; required with --push
  --dockerfile PATH     Dockerfile path (default: Dockerfile)
  --context PATH        Reviewed build context (default: .)
  --push                Push the exact resolved image after a successful build
  --help                Show this help
EOF
}

need_value() {
    if [[ $# -lt 2 || -z "$2" ]]; then
        printf 'missing value for %s\n' "$1" >&2
        exit 2
    fi
}

image_name=""
image_tag=""
registry=""
dockerfile="Dockerfile"
build_context="."
push_requested=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --image)
            need_value "$@"
            image_name="$2"
            shift 2
            ;;
        --tag)
            need_value "$@"
            image_tag="$2"
            shift 2
            ;;
        --registry)
            need_value "$@"
            registry="${2%/}"
            shift 2
            ;;
        --dockerfile)
            need_value "$@"
            dockerfile="$2"
            shift 2
            ;;
        --context)
            need_value "$@"
            build_context="$2"
            shift 2
            ;;
        --push)
            push_requested=true
            shift
            ;;
        --help)
            usage
            exit 0
            ;;
        *)
            printf 'unknown option: %s\n' "$1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

if [[ -z "$image_name" || -z "$image_tag" ]]; then
    usage >&2
    exit 2
fi
if [[ ! "$image_name" =~ ^[a-z0-9]+([._/-][a-z0-9]+)*$ ]]; then
    printf '%s\n' "image name contains unsupported characters" >&2
    exit 2
fi
if [[ ! "$image_tag" =~ ^[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$ ]]; then
    printf '%s\n' "image tag is invalid" >&2
    exit 2
fi
if [[ "$image_tag" == "latest" ]]; then
    printf '%s\n' "refusing mutable tag: latest" >&2
    exit 2
fi
if [[ -n "$registry" &&
      ! "$registry" =~ ^[a-z0-9][a-z0-9.-]*(:[0-9]+)?(/[a-z0-9]+([._-][a-z0-9]+)*)*$ ]]; then
    printf '%s\n' "registry must be a Docker host or host/path, not a URL" >&2
    exit 2
fi
if [[ "$push_requested" == true && -z "$registry" ]]; then
    printf '%s\n' "--push requires --registry" >&2
    exit 2
fi
if [[ ! -f "$dockerfile" || -L "$dockerfile" ]]; then
    printf '%s\n' "dockerfile must be an existing regular non-symlink file" >&2
    exit 2
fi
if [[ ! -d "$build_context" || -L "$build_context" ]]; then
    printf '%s\n' "build context must be an existing non-symlink directory" >&2
    exit 2
fi
if ! command -v docker >/dev/null 2>&1; then
    printf '%s\n' "docker CLI is required" >&2
    exit 2
fi

if [[ -n "$registry" ]]; then
    full_image="${registry}/${image_name}:${image_tag}"
else
    full_image="${image_name}:${image_tag}"
fi

printf 'Building %s\n' "$full_image"
docker build \
    --tag "$full_image" \
    --file "$dockerfile" \
    -- "$build_context"

if [[ "$push_requested" == true ]]; then
    printf 'Pushing %s\n' "$full_image"
    docker push "$full_image"
fi

docker image inspect "$full_image" \
    --format '{{.Id}} {{json .RepoDigests}}'
