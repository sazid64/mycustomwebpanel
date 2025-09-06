#!/usr/bin/env bash
set -e
DOMAIN="$1"
DOCROOT="$2"
CONF_DIR="/usr/local/lsws/conf/vhosts"
VHOST_DIR="$CONF_DIR/$DOMAIN"

mkdir -p "$VHOST_DIR"

cat > "$VHOST_DIR/vhost.conf" <<CONF
docRoot                  $DOCROOT
vhDomain                 $DOMAIN
vhAliases                www.$DOMAIN
errorlog $VHOST_DIR/error.log
accesslog $VHOST_DIR/access.log
index  {
  useServer               0
  indexFiles              index.php, index.html
}
context / {
  type                    static
  location                $DOCROOT
}
CONF

MAIN_CONF="/usr/local/lsws/conf/httpd_config.conf"
if ! grep -q "$CONF_DIR/" "$MAIN_CONF"; then
  echo "include $CONF_DIR/*" >> "$MAIN_CONF"
fi

/usr/local/lsws/bin/lswsctrl restart || true
