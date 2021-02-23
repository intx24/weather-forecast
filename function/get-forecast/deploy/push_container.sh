#!/bin/bash
AWS_ACCOUNT=$(aws sts get-caller-identity --query 'Account' --output text)
docker tag local:get-forecast $AWS_ACCOUNT.dkr.ecr.ap-northeast-1.amazonaws.com/weather-forecast-repo:get-forecast
docker push $AWS_ACCOUNT.dkr.ecr.ap-northeast-1.amazonaws.com/weather-forecast-repo:get-forecast