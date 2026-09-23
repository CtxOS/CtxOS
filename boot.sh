set -e

ascii_art=''

echo -e "$ascii_art"
echo "=> Ctxos is for fresh Ubuntu 24.04 installations only!"
echo -e "\nBegin installation (or abort with ctrl+c)..."

sudo apt-get update >/dev/null
sudo apt-get install -y git >/dev/null

echo "Cloning stable Ctxos..."
rm -rf ~/.local/share/ctxos
git clone -b stable https://github.com/ctxos/ctxos.git ~/.local/share/ctxos >/dev/null

echo "Installation starting..."
source ~/.local/share/ctxos/install.sh
