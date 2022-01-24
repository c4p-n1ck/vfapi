#/bin/bash

# TODO: Custom Ports

export host="127.0.0.1"
export ui_port=8008
export api_port=8888
export script_dir=$PWD


check_ui_stuff() {
	if ! command -v deno >/dev/null; then
		echo "Deno is not found in the path. Shall I install it?"
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
			echo "Please do make sure 'deno' is available in the \$PATH."
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
		figlet -f small "vFAPI"
	else
		echo "     ___ _   ___ ___ "
		echo "__ _| __/_\ | _ \_ _|"
		echo "\ V / _/ _ \|  _/| | "
		echo " \_/|_/_/ \_\_| |___|"
		echo ""
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
	api_check=$(nc -zw5 $host $api_port)
	if [ $? -eq 0 ]; then
		echo "[-] Looks like a service is already running on ://$host:$api_port/"
		if [[ $1 != "--ignore" ]]; then
			exit 1;
		fi
	fi
}


main() {
	# clear
	rm -rf __pycache__/ vfaspi.db*
	banner
	echo -e "\t\tvulnerable FastAPI\n"
	check_ports
	check_ui_stuff
	if [[ $1 == "--dev" ]]; then
		echo "[+] Starting Vulnerable API UI <dev>"
		cd vui && trex run start &
		sleep 0.8
		echo "[+] Starting Vulnerable API <dev"
		cd $script_dir && python3 main.py --dev
	else
		echo "[+] Starting Vulnerable API UI"
		cd vui && snel build && snel serve
		echo "[+] Starting Vulnerable API"
		cd $script_dir && python3 main.py
	fi
}

main $1
