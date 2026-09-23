cat <<EOF >~/.local/share/applications/ctxos.desktop
[Desktop Entry]
Version=1.0
Name=ctxos
Comment=ctxos Project Management
Exec=google-chrome --app="https://launchpad.37signals.com" --name=ctxos
Terminal=false
Type=Application
Icon=/home/$USER/.local/share/ctxos/applications/icons/ctxos.png
Categories=GTK;
MimeType=text/html;text/xml;application/xhtml_xml;
StartupNotify=true
EOF
