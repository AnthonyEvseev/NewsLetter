run:
	docker run -d -p 8000:8000 --env-file .env --name newsletter b4e34ece6ff4

stop:
	docker stop newsletter