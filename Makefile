DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
APP_CONTAINER = main-app
STORAGES_FILE = docker_compose/storages.yaml
STORAGES_CONTAINER = chat-mongodb
KAFKA_FILE = docker_compose/kafka.yaml
KAFKA_CONTAINER =


#all containers
.PHONY: all
all:
	${DC} -f ${APP_FILE} ${ENV} -f ${STORAGES_FILE} ${ENV} -f ${KAFKA_FILE} ${ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${APP_FILE} ${ENV} -f ${STORAGES_FILE} ${ENV} -f ${KAFKA_FILE} ${ENV} down


#app container
.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: app-console
app-console:
	${EXEC} ${APP_CONTAINER} bash


.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest


#storages container
.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: storages-logs
storages-logs:
	${LOGS} ${STORAGES_CONTAINER} -f

# Kafka container
.PHONY: kafka
kafka:
	${DC} -f ${KAFKA_FILE} ${ENV} up --build -d

.PHONY: kafka-down
kafka-down:
	${DC} -f ${KAFKA_FILE} ${ENV} down

.PHONY: kafka-logs
kafka-logs:
	${DC} -f ${KAFKA_FILE} logs -f