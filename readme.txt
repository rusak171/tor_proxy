1. Create an own tor-image with python script to change toridentity
	docker build -t torserv .
2. Run (optional) image through docker
	docker run -it -p 10025:9050 torserv
3. Run several containers through docker-compose
	docker-compose up