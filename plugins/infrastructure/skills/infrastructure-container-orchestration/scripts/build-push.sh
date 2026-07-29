#!/bin/bash
# Build and push Docker image
# Usage: ./build-push.sh [--tag TAG] [--registry REGISTRY] [--push]

set -e

# Defaults
registry="${DOCKER_REGISTRY:-}"
tag="${IMAGE_TAG:-latest}"
push=false
dockerfile="Dockerfile"
context="."

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --tag|-t)
            tag="$2"
            shift 2
            ;;
        --registry|-r)
            registry="$2"
            shift 2
            ;;
        --push|-p)
            push=true
            shift
            ;;
        --dockerfile|-f)
            dockerfile="$2"
            shift 2
            ;;
        --context|-c)
            context="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Get image name from directory or git
if [ -z "$IMAGE_NAME" ]; then
    IMAGE_NAME=$(basename "$(pwd)")
fi

# Build full image name
if [ -n "$registry" ]; then
    full_image="${registry}/${IMAGE_NAME}:${tag}"
else
    full_image="${IMAGE_NAME}:${tag}"
fi

echo "=== Building Docker Image ==="
echo "Image: $full_image"
echo "Dockerfile: $dockerfile"
echo "Context: $context"
echo ""

# Build
docker build \
    -t "$full_image" \
    -f "$dockerfile" \
    --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
    --build-arg VCS_REF="$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')" \
    "$context"

echo ""
echo "=== Build Complete ==="
echo "Image: $full_image"

# Push if requested
if [ "$push" = true ]; then
    echo ""
    echo "=== Pushing Image ==="
    docker push "$full_image"
    echo "Pushed: $full_image"
fi

# Show image info
echo ""
echo "=== Image Info ==="
docker images "$full_image" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
