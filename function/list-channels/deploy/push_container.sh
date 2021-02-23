#!/bin/bash
AWS_ACCOUNT=$(aws sts get-caller-identity --query 'Account' --output text)
docker tag local:list-channels $AWS_ACCOUNT.dkr.ecr.ap-northeast-1.amazonaws.com/weather-forecast-repo:list-channels
docker push $AWS_ACCOUNT.dkr.ecr.ap-northeast-1.amazonaws.com/weather-forecast-repo:list-channels