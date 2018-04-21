
PYDEV_IMAGE = tigerbot/pydev

pydev-image:
	docker build -f Dockerfile -t $(PYDEV_IMAGE) .

run-container:
	docker run -ti --device=/dev/vcsm --device=/dev/vchiq \
		--net=host \
		-e DISPLAY=$$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
		-v /home/pi:/home/pi -w `pwd` \
		-e XAUTHORITY=/home/pi/.Xauthority \
	        -v `pwd`/../cfg:/cfg \
		$(PYDEV_IMAGE)
