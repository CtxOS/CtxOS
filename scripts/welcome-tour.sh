#!/usr/bin/env bash
# welcome-tour.sh - A celebratory interactive tour of CtxOS
set -e

# Visual Helpers
COLOR_BLUE="\033[0;34m"
COLOR_CYAN="\033[0;36m"
COLOR_GREEN="\033[0;32m"
COLOR_MAGENTA="\033[0;35m"
COLOR_YELLOW="\033[1;33m"
COLOR_RESET="\033[0m"

clear

echo -e "${COLOR_CYAN}====================================================${COLOR_RESET}"
echo -e "${COLOR_CYAN}   🚀 WELCOME TO THE CTXOS LAUNCH EVENT   ${COLOR_RESET}"
echo -e "${COLOR_CYAN}====================================================${COLOR_RESET}"
echo ""

sleep 1
echo -e "${COLOR_YELLOW}[1/5] The Architecture${COLOR_RESET}"
echo -e "Implementing a secure DBus API layer... ${COLOR_GREEN}DONE${COLOR_RESET}"
echo -e "Gating system actions with Polkit... ${COLOR_GREEN}DONE${COLOR_RESET}"
echo ""

sleep 1.5
echo -e "${COLOR_YELLOW}[2/5] The Hybrid Engine${COLOR_RESET}"
echo -e "Bridging APT, Flatpak, and Meta-Packages... ${COLOR_GREEN}ACTIVE${COLOR_RESET}"
echo -e "AppStream metadata integration... ${COLOR_GREEN}READY${COLOR_RESET}"
echo ""

sleep 1.5
echo -e "${COLOR_YELLOW}[3/5] System Resilience${COLOR_RESET}"
echo -e "Snapshot protection (Timeshift/Snapper)... ${COLOR_BLUE}SHIELD ACTIVE${COLOR_RESET}"
echo -e "Automated health validation... ${COLOR_BLUE}VITAL SIGNS OK${COLOR_RESET}"
echo ""

sleep 1.5
echo -e "${COLOR_YELLOW}[4/5] Global Reach & Identity${COLOR_RESET}"
echo -e "Localization Engine (English/Spanish)... ${COLOR_MAGENTA}READY${COLOR_RESET}"
echo -e "OEM Branding Overrides... ${COLOR_MAGENTA}CONFIGURABLE${COLOR_RESET}"
echo ""

sleep 1.5
echo -e "${COLOR_YELLOW}[5/5] Portability${COLOR_RESET}"
echo -e "Docker, VM, and WSL Support... ${COLOR_GREEN}FULL SUPPORT${COLOR_RESET}"
echo ""

sleep 2
echo -e "${COLOR_CYAN}----------------------------------------------------${COLOR_RESET}"
echo -e "   CtxOS is now officially ENGINEERED."
echo -e "${COLOR_CYAN}----------------------------------------------------${COLOR_RESET}"
echo ""
echo -e "Run ${COLOR_GREEN}./scripts/pipeline-master.sh patch${COLOR_RESET} to launch your first release!"
echo ""
echo -e "${COLOR_YELLOW}Happy Distro Building! 🏁✨${COLOR_RESET}"
echo ""
