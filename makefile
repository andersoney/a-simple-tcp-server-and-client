run_serve:
	python tcp_server.py 9089 dir_path

run_client:
	python tcp_client.py 192.168.0.103 9089 1.log
run_client_list:
	python tcp_client.py 192.168.0.103 9089 list

run_client_exe:
	./tcp_client.exe 192.168.0.103 9089 1.log
run_client_exe_list:
	./tcp_client.exe 192.168.0.103 9089 list
run_serve_exe:
	./tcp_server.exe 9089 dir_path

build_exe:
	rm -rf dist build
	pip install pyinstaller
	pyinstaller --onefile tcp_client.py
	pyinstaller --onefile tcp_server.py
	rm -rf tcp_client.spec tcp_server.spec build
	mv dist/tcp_client.exe tcp_client.exe
	mv dist/tcp_server.exe tcp_server.exe
	rm -rf dist
	rm -rf dir_path_received
