export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1

usage: ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/$$//' | sed -e 's/##//'

start_localstack: ## Start Localstack services
	docker-compose up -d --force-recreate

iac_lint: ## Verify IaC (MUST BE USED BEFORE DEPLOY)
	cfn-lint template.yaml


full_deploy: start_localstack iac_lint create_ssm_parameter create_secrets_manager build deploy
