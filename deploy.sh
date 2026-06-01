#!/usr/bin/env bash
set -euo pipefail

# Deploys the BCR backend as a systemd service so it starts on boot
# and is automatically restarted if it crashes or the VM reboots.
#
# Usage:
#   ./deploy.sh              # install/update and start the service
#   ./deploy.sh status       # show service status
#   ./deploy.sh logs         # tail service logs
#   ./deploy.sh restart      # restart the service
#   ./deploy.sh stop         # stop the service (does not disable autostart)
#   ./deploy.sh uninstall    # stop, disable, and remove the service

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICE_NAME="bcr-backend"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
RUN_USER="$(id -un)"
RUN_GROUP="$(id -gn)"
PORT="${PORT:-5050}"

cmd="${1:-install}"

case "$cmd" in
  status)
    exec sudo systemctl status "$SERVICE_NAME" --no-pager
    ;;
  logs)
    exec sudo journalctl -u "$SERVICE_NAME" -f --no-pager
    ;;
  restart)
    sudo systemctl restart "$SERVICE_NAME"
    sudo systemctl status "$SERVICE_NAME" --no-pager
    exit 0
    ;;
  stop)
    sudo systemctl stop "$SERVICE_NAME"
    exit 0
    ;;
  uninstall)
    sudo systemctl disable --now "$SERVICE_NAME" 2>/dev/null || true
    sudo rm -f "$SERVICE_FILE"
    sudo systemctl daemon-reload
    echo "Removed $SERVICE_NAME."
    exit 0
    ;;
  install|"")
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    echo "Usage: $0 [install|status|logs|restart|stop|uninstall]" >&2
    exit 1
    ;;
esac

echo "==> Preparing virtual environment in $APP_DIR/venv"
cd "$APP_DIR"
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
# shellcheck disable=SC1091
source venv/bin/activate
pip install --upgrade pip >/dev/null
pip install -r requirements.txt
pip install gunicorn

VENV_PYTHON="$APP_DIR/venv/bin/python"
GUNICORN="$APP_DIR/venv/bin/gunicorn"

if [ ! -f "instance/bcr.db" ] && [ ! -f "instance/app.db" ]; then
  echo "==> No database found, seeding..."
  "$VENV_PYTHON" seed.py || echo "WARN: seed.py failed; continuing."
fi

echo "==> Writing systemd unit to $SERVICE_FILE"
sudo tee "$SERVICE_FILE" >/dev/null <<EOF
[Unit]
Description=BCR Backend (Flask via gunicorn)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${RUN_USER}
Group=${RUN_GROUP}
WorkingDirectory=${APP_DIR}
Environment=PORT=${PORT}
Environment=PYTHONUNBUFFERED=1
ExecStart=${GUNICORN} --workers 3 --bind 0.0.0.0:${PORT} --access-logfile - --error-logfile - run:app
Restart=always
RestartSec=5
StartLimitIntervalSec=0

[Install]
WantedBy=multi-user.target
EOF

echo "==> Enabling and starting $SERVICE_NAME"
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

sleep 1
sudo systemctl status "$SERVICE_NAME" --no-pager || true

echo
echo "Done. Service '$SERVICE_NAME' is enabled (auto-starts on boot) and running on port ${PORT}."
echo "  Logs:    ./deploy.sh logs"
echo "  Status:  ./deploy.sh status"
echo "  Restart: ./deploy.sh restart"
