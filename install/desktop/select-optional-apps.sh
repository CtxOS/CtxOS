if [[ -v CTXOS_FIRST_RUN_OPTIONAL_APPS ]]; then
	apps=$CTXOS_FIRST_RUN_OPTIONAL_APPS

	if [[ -n "$apps" ]]; then
		for app in $apps; do
			source "$CTXOS_PATH/install/desktop/optional/app-${app,,}.sh"
		done
	fi
fi
