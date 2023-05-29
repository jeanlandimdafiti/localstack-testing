export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1

usage:           ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/$$//' | sed -e 's/##//'

start_localstack: ## Start Localstack
	docker-compose up -d --force-recreate

iac_lint: ## Verify IaC
	cfn-lint template.yaml

create_ssm_parameter: 
	awslocal ssm put-parameter --name "environment" --type "String" --value "local"

create_secrets_manager:
	awslocal secretsmanager create-secret --name vault --secret-string '[{"url":"http://foo", "token": "123", "mount-point": "123" }]'

build: ## Build
	samlocal build --use-container

deploy: ## Deploy the app
	echo "Deploying Serverless app to local environment"; 
	samlocal deploy --template-file template.yaml --stack-name braze-update-workflow --resolve-s3 --debug --capabilities CAPABILITY_IAM  --parameter-overrides environment=local 

start_state_machine:
	awslocal stepfunctions start-execution --name braze--update-workflow --state-machine-arn arn:aws:states:us-east-1:000000000000:stateMachine:braze-update-workflow --input '{"request_type": "canvas_trigger_send", "message_body": "one-two-three"}'

describe_state_machine:
	awslocal stepfunctions describe-execution --execution-arn arn:aws:states:us-east-1:000000000000:execution:braze-update-workflow:braze-update-workflow

full_deploy: start_localstack iac_lint create_ssm_parameter create_secrets_manager build deploy
