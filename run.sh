#/bin/bash

stty -echoctl

# TODO: Custom Ports

export DENO_INSTALL="/home/$USER/.deno"
export PATH="$DENO_INSTALL/bin:$PATH"
export host="127.0.0.1"
export ui_port=8008
export api_port=8888
export script_dir=$PWD


quit() {
    tput setaf 1
    rm -rf __pycache__/ vfapi.*.db &
    printf "\n[!] SIGINT trapped, terminating..\n\n"
    tput sgr0
    sleep 0.48
    exit 0
}; trap 'quit' SIGINT


check_ui_stuff() {
	if [ "$(ls -A ./vui)" ] ;then
		printf "\n[!] Updating (if any) Vulnerable UI (vui) over git.\n"
		cd vui && git pull $(git remote get-url origin) &>/dev/null && cd - >/dev/null
	else
		printf "\n[!] Downloading Vulnerable User Interface (vui) over git.\n"
		git submodule init
		git submodule update
		echo ""
	fi
	if ! command -v deno >/dev/null; then
		echo "[-] Deno is not found in the path. Shall I install it?"
		echo -n "[y/N]: "
		read prompt
		if [[ $prompt == "y" || $prompt == "Y" ]]; then
			echo "[+] Installing deno."
			curl -fsSL https://deno.land/install.sh | sh
			export DENO_INSTALL="/home/$USER/.deno"
			export PATH="$DENO_INSTALL/bin:$PATH"
			shells="bash zsh"
			for shell in $shells; do
				dot_filename="$HOME/.${shell}rc"
				test -f $dot_filename && echo -e "export DENO_INSTALL=\"/home/\$USER/.deno\"\nexport PATH=\"\$DENO_INSTALL/bin/:\$PATH\"" >> "$dot_filename"
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
	if ! command -v file_server >/dev/null; then
		echo "[+] Installing HTTP 'file_server' (deno)"
		deno install --allow-net --allow-read https://deno.land/std@0.106.0/http/file_server.ts
	fi
}


banner () {
	if command -v figlet >/dev/null; then
		figlet -f small "vFAPI"
	else
		echo "     ___ _   ___ ___ "
		echo "__ _| __/_\ | _ \_ _|"
		echo "\ V / _/ _ \|  _/| | "
		echo " \_/|_/_/ \_\_| |___|"
	fi
}


check_ports() {
	# TODO: fix code-repetition
	ui_check=$(nc -zw5 $host $ui_port)
	if [[ $? -eq 0 ]]; then
		echo "[-] Looks like port ://$host:$ui_port/ is already occupied. Please kill/stop the running service conflicting the port number."
		if [[ $1 != "--ignore" ]]; then
			exit 1;
		fi
	fi
	api_check=$(nc -zw5 $host $api_port)
	if [ $? -eq 0 ]; then
		echo "[-] Looks like a service is already running on ://$host:$api_port/"
		if [[ $1 != "--ignore" ]]; then
			exit 1;
		fi
	fi
}


main() {
	rm -rf __pycache__/ vfapi.*.db
	banner
	printf "\t\tvulnerable FastAPI\n"
	check_ports
	check_ui_stuff
	sleep 0.48
	echo "[+] Compiling User Interface"
	deno compile -Ar --unstable vulnerable_user_interface.ts >/dev/null;
	if [[ $1 == "--dev" ]]; then
		printf "[!] Starting Vulnerable API <dev>\n"
		cd $script_dir && python3 main.py --dev &
		sleep 0.84
		while :; do
			printf "\n[!] Starting Vulnerable API UI <dev>\n"
			cd vui && trex run start &
			./vulnerable_user_interface
			cd $script_dir
		done
	else
		printf "[+] Starting Vulnerable API\n"
		cd $script_dir && python3 main.py &
		printf "[+] Starting Vulnerable API UI\n"
		cd vui && snel build && cd dist && file_server --host 127.0.0.1 -p 8008 &
		cd $script_dir && ./vulnerable_user_interface && rm -rf __pycache__/ vfapi.*.db
	fi
}

main $1
