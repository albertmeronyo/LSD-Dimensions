#!/bin/bash
set -e
LSD_CLONE_URL=https://github.com/albertmeronyo/LSD-Dimensions.git

## Execute a command as GITLAB_USER
exec_as_lsd() {
  if [[ $(whoami) == ${LSD_USER} ]]; then
    $@
  else
    sudo -HEu ${LSD_USER} "$@"
  fi
}

#add grlc user
adduser --disabled-login --gecos 'lsd' ${LSD_USER}
passwd -d ${LSD_USER}

#configure git
exec_as_lsd git config --global core.autocrlf input
exec_as_lsd git config --global gc.auto 0



exec_as_lsd git clone ${LSD_CLONE_URL} ${LSD_INSTALL_DIR}
cd ${LSD_INSTALL_DIR}
pip install -r requirements.txt

#move nginx logs to ${GITLAB_LOG_DIR}/nginx
sed -i \
 -e "s|access_log /var/log/nginx/access.log;|access_log ${LSD_LOG_DIR}/nginx/access.log;|" \
 -e "s|error_log /var/log/nginx/error.log;|error_log ${LSD_LOG_DIR}/nginx/error.log;|" \
 /etc/nginx/nginx.conf


 # configure gitlab log rotation
 cat > /etc/logrotate.d/lsd << EOF
 ${LSD_LOG_DIR}/lsd/*.log {
   weekly
   missingok
   rotate 52
   compress
   delaycompress
   notifempty
   copytruncate
 }
 EOF

 # configure gitlab vhost log rotation
 cat > /etc/logrotate.d/lsd-nginx << EOF
 ${LSD_LOG_DIR}/lsd/*.log {
   weekly
   missingok
   rotate 52
   compress
   delaycompress
   notifempty
   copytruncate
 }
 EOF
