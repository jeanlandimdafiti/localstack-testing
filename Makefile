export AWS_ACCESS_KEY_ID ?= test
export AWS_SECRET_ACCESS_KEY ?= test
export AWS_DEFAULT_REGION = us-east-1

usage:           ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

start_localstack: ## Start Localstack
	docker-compose up -d --force-recreate

build:
	samlocal build --use-container

deploy:          ## Deploy the app
	echo "Deploying Serverless app to local environment"; \
	samlocal deploy --template-file template.yaml --stack-name campaign-segmentation-workflow --resolve-s3 --debug --capabilities CAPABILITY_IAM 
	
