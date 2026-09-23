# Gum is used for the Ctxos commands for tailoring Ctxos after the initial install
cd /tmp
GUM_VERSION="0.14.1" # Use known good version
wget -qO gum.deb "https://github.com/charmbracelet/gum/releases/latest/download/gum_${GUM_VERSION}_amd64.deb"
sudo apt-get install -y ./gum.deb
rm gum.deb
cd -
