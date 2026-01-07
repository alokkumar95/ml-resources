## Docker Commands
- start the servers - `docker compose up -d`
- verify the setup - `docker ps`
- stop and remove the server - `docker compose down`
- only stop them without deleting them - `docker compose stop` 
- start if already created - `docker compose -f docker-compose.prod.yml start`
- if you have multiple compose file - `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d`
- view logs from terminal - `docker compose logs -f`
- view logs of particular server - `docker compose logs -f server1`


## Tracking Performace Metrics
- request_time - `docker compose logs -f load_balancer | grep -E '"request_time":"[1-9]\.[5-9]|[2-9]\.'`
- 

## Configuring SSL/TLS for HTTPS traffice
- Generate a local certificate - `openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx.key -out nginx.crt -subj "/CN=localhost"`
- 

## Further Readings
- Nginx - https://nginx.org/en/
- Log Monitoring - https://clickhouse.com/resources/engineering/log-monitoring
- ServerVault - https://serverfault.com/questions/690239/does-nginx-keep-the-connection-open-when-it-does-load-balancing
- AiKNOW - https://www.aiknow.io/en/what-is-nginx-and-what-is-it-for/?doing_wp_cron=1785681128.0934050083160400390625

