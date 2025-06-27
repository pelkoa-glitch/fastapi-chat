DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env

APP_DEV = docker_compose/app.dev.yaml
APP_CONTAINER = main-app
KAFKA = docker_compose/kafka.yaml
MONGO = docker_compose/mongo.yaml
MONGO_EXPRESS = docker_compose/mongo-express.yaml
MONITORING_FILE = docker_compose/monitoring.yaml


# All containers, except monitoring
.PHONY: all
all:
	${DC} -f ${APP_DEV} ${ENV}  -f ${KAFKA} ${ENV}  -f ${MONGO} ${ENV} -f ${MONGO_EXPRESS} ${ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${APP_DEV} -f ${KAFKA} -f ${MONGO} -f ${MONGO_EXPRESS} ${ENV} down


# App
.PHONY: app
app:
	${DC} -f ${APP_DEV} -f ${KAFKA} ${ENV} up --build -d

.PHONY: app-logs
app-logs:
	${LOGS} -f ${APP_CONTAINER} -f

.PHONY: app-down
down-dev:
	${DC} -f ${APP_DEV} -f ${KAFKA} ${ENV} down


# Kafka
.PHONY: kafka
kafka:
	${DC} -f ${KAFKA} ${ENV} up --build -d

.PHONY: kafka-down
kafka-down:
	${DC} -f ${KAFKA} ${ENV} down


# Mongo db
.PHONY: storages
storages:
	${DC} -f ${MONGO} ${ENV} up --build -d

.PHONY: ui
ui:
	${DC} -f ${MONGO_EXPRESS} ${ENV} up --build -d


# Elastic Apm, Elasticsearch, Kibana
.PHONY: monitoring-logs
monitoring-logs:
	${DC} -f ${MONITORING_FILE} ${ENV} logs -f

.PHONY: monitoring
monitoring:
	${DC} -f ${MONITORING_FILE} ${ENV} up --build -d

.PHONY: monitoring-down
monitoring-down:
	${DC} -f ${MONITORING_FILE} ${ENV} down



# Clear all volumes
.PHONY: purge
purge:
	${DC} -f ${KAFKA} -f ${MONGO} -f ${MONGO_EXPRESS} ${ENV} down -v

# Command line inside app container
.PHONY: shell
shell:
	${EXEC} ${APP_CONTAINER} bash

# Run app tests
.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest -v
