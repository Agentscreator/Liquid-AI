#!/usr/bin/env bash
#
# deploy-digitalocean.sh — Deploy Liquid to DigitalOcean App Platform
#
# Prerequisites:
#   1. doctl CLI installed and authenticated (doctl auth init)
#   2. A DigitalOcean account with App Platform access
#   3. Your GRADIENT_MODEL_ACCESS_KEY from the Gradient AI Platform
#
# Usage:
#   ./deploy-digitalocean.sh                                          # interactive
#   GRADIENT_MODEL_ACCESS_KEY=xxx ./deploy-digitalocean.sh            # non-interactive
#

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

# ── Preflight checks ────────────────────────────────────────
if ! command -v doctl &>/dev/null; then
  echo -e "${RED}doctl CLI not found.${NC}"
  echo "Install it from https://docs.digitalocean.com/reference/doctl/how-to/install/"
  exit 1
fi

# Resolve Gradient key
GRADIENT_MODEL_ACCESS_KEY="${GRADIENT_MODEL_ACCESS_KEY:-}"
GRADIENT_AGENT_ACCESS_KEY="${GRADIENT_AGENT_ACCESS_KEY:-}"

if [ -z "$GRADIENT_MODEL_ACCESS_KEY" ]; then
  if [ -f .env ]; then
    GRADIENT_MODEL_ACCESS_KEY=$(grep -E '^GRADIENT_MODEL_ACCESS_KEY=' .env | cut -d= -f2- | tr -d '"' || true)
  fi
  if [ -z "$GRADIENT_MODEL_ACCESS_KEY" ]; then
    read -rsp "Enter your GRADIENT_MODEL_ACCESS_KEY: " GRADIENT_MODEL_ACCESS_KEY
    echo
  fi
fi

if [ -z "$GRADIENT_MODEL_ACCESS_KEY" ]; then
  echo -e "${RED}GRADIENT_MODEL_ACCESS_KEY is required.${NC}"
  echo "Get one from https://cloud.digitalocean.com/gradient-ai/serverless-inference"
  exit 1
fi

echo -e "${GREEN}Gradient key:${NC} ****${GRADIENT_MODEL_ACCESS_KEY: -4}"
echo

# ── Deploy via App Platform ─────────────────────────────────
echo -e "${BOLD}Deploying to DigitalOcean App Platform...${NC}"

# Create app spec on the fly
APP_SPEC=$(cat <<EOF
{
  "spec": {
    "name": "liquid-ai",
    "region": "nyc",
    "services": [
      {
        "name": "liquid",
        "dockerfile_path": "Dockerfile",
        "github": {
          "repo": "Agentscreator/Liquid-AI",
          "branch": "main",
          "deploy_on_push": true
        },
        "http_port": 8787,
        "instance_count": 1,
        "instance_size_slug": "professional-xs",
        "envs": [
          {
            "key": "GRADIENT_MODEL_ACCESS_KEY",
            "value": "${GRADIENT_MODEL_ACCESS_KEY}",
            "type": "SECRET"
          }
        ],
        "health_check": {
          "http_path": "/api/health"
        }
      }
    ]
  }
}
EOF
)

echo "$APP_SPEC" | doctl apps create --spec -

echo
echo -e "${GREEN}${BOLD}Deployed!${NC}"
echo
echo "View your app at: https://cloud.digitalocean.com/apps"
echo "The app will build and deploy automatically from the main branch."
