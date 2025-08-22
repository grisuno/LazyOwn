sudo apt-get install jq
chmod +x mkdocker.sh
./mkdocker.sh build
./mkdocker.sh run --vpn 1
#aws ecr create-repository --repository-name lazyown
#docker tag lazyown:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/lazyown:latest
#docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/lazyown:latest
