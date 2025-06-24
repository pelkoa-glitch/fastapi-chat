DC = docker compose
APP_DEV = docker_compose/app.dev.yaml
EXEC = docker exec -it
LOGS = docker logs
KAFKA = docker_compose/kafka.yaml
MONGO = docker_compose/mongo.yaml
MONGO_EXPRESS = docker_compose/mongo-express.yaml
APP_CONTAINER = main-app
ENV = --env-file .env


.PHONY: all
all:
	${DC} -f ${APP_DEV} ${ENV}  -f ${KAFKA} ${ENV}  -f ${MONGO} ${ENV} -f ${MONGO_EXPRESS} ${ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${APP_DEV} -f ${KAFKA} -f ${MONGO} -f ${MONGO_EXPRESS} ${ENV} down

.PHONY: app
app:
	${DC} -f ${APP_DEV} -f ${KAFKA} ${ENV} up --build -d

.PHONY: app-logs
app-logs:
	${LOGS} -f ${APP_CONTAINER} -f

.PHONY: storages
storages:
	${DC} -f ${MONGO} ${ENV} up --build -d

.PHONY: app-down
down-dev:
	${DC} -f ${APP_DEV} -f ${KAFKA} ${ENV} down

.PHONY: down
down:
	${DC} -f ${APP_DEV} -f ${KAFKA} -f ${MONGO} -f ${MONGO_EXPRESS} ${ENV} down

.PHONY: ui
ui:
	${DC} -f ${MONGO_EXPRESS} ${ENV} up --build -d

.PHONY: purge
purge:
	${DC} -f ${KAFKA} -f ${MONGO} -f ${MONGO_EXPRESS} ${ENV} down -v

.PHONY: shell
shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest -s