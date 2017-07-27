all:
	python3 main.py

trans:
	python3 update_trans.py

deploy:
	buildozer android debug deploy run

log:
	# sudo apt-get install adb
	rm logcat.txt
	adb logcat > logcat.txt
