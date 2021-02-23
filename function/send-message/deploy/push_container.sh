#!/bin/bash
AWS_ACCOUNT=$(aws sts get-caller-identity --query 'Account' --output text)
docker tag local:send-message $AWS_ACCOUNT.dkr.ecr.ap-northeast-1.amazonaws.com/weather-forecast-repo:send-message
docker push $AWS_ACCOUNT.dkr.ecr.ap-northeast-1.amazonaws.com/weather-forecast-repo:send-message