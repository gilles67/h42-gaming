wheels:
	apt-get update -y
	apt-get upgrade -y
	apt-get install -y --no-install-recommends python3 python3-distutils python3-dev python3-pip libssl-dev openssl libacl1-dev libacl1 build-essential pkg-config openssh-client tzdata
	mkdir -p /opt/wheels 
	pip3 wheel -v -r /h42gaming/requirements.txt --wheel-dir=/opt/wheels

setup:
	apt-get update -y
	apt-get upgrade -y
	apt-get install -y --no-install-recommends python3 python3-paho-mqtt python3-zmq python3-distutils python3-pip tzdata
	apt-get -y autoremove
	apt-get clean
	pip3 install -v --no-index --find-links=/opt/wheels -r /h42gaming/requirements.txt

	apt-get -y autoremove
	apt-get -y clean
	apt-get -y autoclean

	chmod a+x /h42gaming/run-console