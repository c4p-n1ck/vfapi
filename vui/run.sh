#/bin/bash

stty -echoctl

# TODO: Custom Ports

export host="127.0.0.1"
export ui_port=8008


quit() {
    tput setaf 1
    rm -rf __pycache__/ vfapi.*.db &
    printf "\n[!] SIGINT trapped, terminating..\n\n"
    tput sgr0
    sleep 0.48
    exit 0
}; trap 'quit' SIGINT


check_dependencies() {
	if ! command -v deno >/dev/null; then
		echo "[-] Deno is not found in the path. Shall I install it?"
		echo -n "[y/N]: "
		read prompt
		if [[ $prompt == "y" || $prompt == "Y" ]]; then
			echo "[+] Installing deno."
			curl -fsSL https://deno.land/install.sh | sh
			export DENO_INSTALL="/home/$USER/.deno"
			export PATH="$DENO_INSTALL/bin:$PATH"
			shells = "bash zsh"
			for shell in $shells; do
				dot_filename="~/.${shell}rc"
				test -f $dot_filename && echo "export DENO_INSTALL="/home/\$USER/.deno\nexport PATH="\$DENO_INSTALL/bin/:\$PATH" >> $dot_filename
			done
		else
			echo "[!] Please do make sure 'deno' is available in the \$PATH."
			exit 1
		fi
	fi
	if ! command -v snel >/dev/null; then
		echo "[+] Installing 'snel' (svelte for deno)"
		deno run --allow-run --allow-read https://deno.land/x/snel/install.ts
	fi
}


banner () {
	if command -v figlet >/dev/null; then
		figlet -f small "vUI"
	else
		echo "      _   _ ___ "
 		echo " __ _| | | |_ _|"
 		echo " \ V / |_| || | "
		echo "  \_/ \___/|___|"
	fi
}


check_ports() {
	ui_check=$(nc -zw5 $host $ui_port)
	if [[ $? -eq 0 ]]; then
		echo "[-] Looks like port ://$host:$ui_port/ is already occupied. Please kill/stop the running service conflicting the port number."
		if [[ $1 != "--ignore" ]]; then
			exit 1;
		fi
	fi
}


main() {
	rm -rf __pycache__/ vfapi.*.db
	banner
	printf "\t\tvulnerable User Interface\n"
	check_ports
	check_dependencies
	sleep 0.48
	if [[ $1 == "--dev" ]]; then
		while :; do
			printf "\n[!] Starting Vulnerable API UI <dev>\n"
			trex run start
		done
	else
		printf "\n[+] Starting Vulnerable API UI\n\n"
		snel build  # TODO: Serve the built files.
	fi
}

main --dev
