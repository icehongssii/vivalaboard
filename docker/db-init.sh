#!/bin/bash

# 기본 entrypoint를 실행하여 디비 서버를 시작.
/usr/local/bin/docker-entrypoint.sh mysqld &

# 서버가 실행되기를 기다림
until mysqladmin ping -uroot -p"$MYSQL_ROOT_PASSWORD" --silent; do
  echo 'Waiting for MySQL to become available...'
  sleep 1
done

# init.sql을 실행
echo 'Executing init.sql...'
mysql -uroot -p"$MYSQL_ROOT_PASSWORD" --port 3306 "$MYSQL_DATABASE" < /docker-entrypoint-initdb.d/init.sql

# 컨테이너가 종료될 때까지 
wait