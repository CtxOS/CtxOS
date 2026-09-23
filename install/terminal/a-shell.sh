# Configure the bash shell using Ctxos defaults
[ -f "~/.bashrc" ] && mv ~/.bashrc ~/.bashrc.bak
cp ~/.local/share/ctxos/configs/bashrc ~/.bashrc

# Load the PATH for use later in the installers
source ~/.local/share/ctxos/defaults/bash/shell

[ -f "~/.inputrc" ] && mv ~/.inputrc ~/.inputrc.bak
# Configure the inputrc using Ctxos defaults
cp ~/.local/share/ctxos/configs/inputrc ~/.inputrc
