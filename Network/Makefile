help:
	@echo " "
	@echo "Welcome to the Beacon deployment makefile."
	@echo "------------------------------------------"
	@echo " "
	@echo "Here are all your options:"
	@echo "help \t\t- Show this help message"
	@echo "build-db \t- It will create and fill a PostgreSQL database"
	@echo "run-db \t\t- Run the created PostgreSQL database on port 5432"
	@echo "clean-db \t- Remove containers and images from DB deployment"

build-db:
	docker-compose -f ./db/docker-compose.yml build db

run-db:
	docker-compose -f ./db/docker-compose.yml up -d

clean-db:
	docker-compose -f ./db/docker-compose.yml down -v
