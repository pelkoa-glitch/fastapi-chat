#!/bin/bash


sleep 5 #TODO: написать нормальный энтрипоинт

uvicorn --factory application.api.main:create_app --timeout-graceful-shutdown 2 --reload --host 0.0.0.0 --port 8000
