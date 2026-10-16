#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./release.sh [VERSION] [--push]

Examples:
  ./release.sh             # calcula la siguiente version con git-cliff
  ./release.sh v0.1.1      # fuerza una version concreta
  ./release.sh --push      # crea release y hace push de commit + tag
  ./release.sh v0.1.1 --push
EOF
}

PUSH=false
VERSION=""

for arg in "$@"; do
  case "$arg" in
    -h|--help)
      usage
      exit 0
      ;;
    --push)
      PUSH=true
      ;;
    *)
      if [[ -n "$VERSION" ]]; then
        echo "Error: version duplicada o argumento desconocido: $arg" >&2
        usage >&2
        exit 1
      fi
      VERSION="$arg"
      ;;
  esac
done

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Error: falta '$1' en PATH" >&2
    exit 1
  fi
}

require_cmd git
require_cmd git-cliff

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

if [[ ! -f cliff.toml ]]; then
  echo "Error: no encuentro cliff.toml en $ROOT" >&2
  exit 1
fi

CURRENT="$(git branch --show-current)"
if [[ "$CURRENT" != "master" ]]; then
  echo "Error: la release se corta desde 'master' (rama actual: ${CURRENT:-detached})." >&2
  echo "Haz merge de dev a master primero." >&2
  exit 1
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Error: el working tree no esta limpio." >&2
  echo "Haz commit/stash de tus cambios antes de crear la release." >&2
  git status --short >&2
  exit 1
fi

if [[ -z "$VERSION" ]]; then
  VERSION="$(git cliff --bumped-version | tail -n 1 | tr -d '[:space:]')"
fi

if [[ ! "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+([-.][0-9A-Za-z.-]+)?$ ]]; then
  echo "Error: version invalida: '$VERSION' (esperado: vMAJOR.MINOR.PATCH)" >&2
  exit 1
fi

if git rev-parse -q --verify "refs/tags/$VERSION" >/dev/null; then
  echo "Error: el tag $VERSION ya existe" >&2
  exit 1
fi

LATEST_TAG="$(git tag --list 'v*' --sort=-v:refname | head -n 1 || true)"

echo "Ultimo tag: ${LATEST_TAG:-ninguno}"
echo "Nueva version: $VERSION"

git cliff --config cliff.toml --tag "$VERSION" --output CHANGELOG.md

git add CHANGELOG.md

if git diff --cached --quiet; then
  echo "No hay cambios de changelog para commitear."
else
  git commit -m "chore(release): $VERSION"
fi

git tag -a "$VERSION" -m "Release $VERSION"

echo "Release creada: $VERSION"

if [[ "$PUSH" == true ]]; then
  CURRENT_BRANCH="$(git branch --show-current)"
  if [[ -z "$CURRENT_BRANCH" ]]; then
    echo "Error: no puedo hacer push desde detached HEAD" >&2
    exit 1
  fi
  git push origin "$CURRENT_BRANCH"
  git push origin "$VERSION"
  echo "Push completado: origin/$CURRENT_BRANCH + $VERSION"
else
  echo "Para publicar: git push origin $(git branch --show-current) && git push origin $VERSION"
fi
