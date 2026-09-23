cat <<EOF >~/.local/share/applications/Ctxos.desktop
[Desktop Entry]
Version=1.0
Name=Ctxos
Comment=Ctxos Controls
Exec=alacritty --config-file /home/$USER/.local/share/ctxos/defaults/alacritty/pane.toml -e ctxos
Terminal=false
Type=Application
Icon=/home/$USER/.local/share/ctxos/applications/icons/Ctxos.png
Categories=GTK;
StartupNotify=false
EOF
