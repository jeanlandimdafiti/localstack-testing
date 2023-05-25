ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
STATE_MACHINE_NAME=braze_update_workflow
STATE_MACHINE_EVENTS=file://statemachine/test/events
STATE_MACHINE_DEFINITION_FILE=file://../src/statemachine/${STATE_MACHINE_NAME}.asl.json
STATE_MACHINE_ARN=arn:aws:states:ap-southeast-2:123456789013:stateMachine:${STATE_MACHINE_NAME}
STATE_MACHINE_EXECUTION_ARN=arn:aws:states:ap-southeast-2:123456789013:execution:${STATE_MACHINE_NAME}
WAIT_TIME=$(shell date --utc +%FT%T.%3NZ -d '1 mins')


run:
	docker-compose up -d --force-recreate 
	sleep 2 

create:
	aws stepfunctions create-state-machine \
		--endpoint-url http://localhost:8083 \
		--definition  ${STATE_MACHINE_DEFINITION_FILE}\
		--name ${STATE_MACHINE_NAME} \
		--role-arn "arn:aws:iam::123456789012:role/DummyRole" \
		--no-cli-pager
		
execute_best_scenario:
	aws stepfunctions start-execution \
		--endpoint http://localhost:8083 \
		--name BestScenario \
		--state-machine ${STATE_MACHINE_ARN}#BestScenario\
		--input ${STATE_MACHINE_EVENTS}/canvas_trigger_send.json\
		--no-cli-pager

execute_wait_scenario:
	aws stepfunctions start-execution \
		--endpoint http://localhost:8083 \
		--name WaitScenario \
		--state-machine ${STATE_MACHINE_ARN}#WaitScenario\
		--input ${STATE_MACHINE_EVENTS}/canvas_trigger_send.json\
		--no-cli-pager

test_best_scenario:
	aws stepfunctions describe-execution \
		--endpoint http://localhost:8083 \
		--execution-arn ${STATE_MACHINE_EXECUTION_ARN}:BestScenario \
		--no-cli-pager

test_wait_scenario:
	aws stepfunctions describe-execution \
		--endpoint http://localhost:8083 \
		--execution-arn ${STATE_MACHINE_EXECUTION_ARN}:WaitScenario \
		--no-cli-pager

describe_sf:
	aws stepfunctions describe-state-machine \
	--endpoint http://localhost:8083 \
	--state-machine-arn ${STATE_MACHINE_ARN} \
	--no-cli-pager
	
	
