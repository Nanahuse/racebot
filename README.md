# racebot
Discordでレース用のカウントダウンを行うためのBotです。

# Command
* !rc
* !vrc
* !help


# docker-compose.yaml sample
## deploy on dockge
```yaml
services:
  main:
    restart: always
    image: ghcr.io/nanahuse/racebot:latest
    environment:
      # requires
      - BOT_TOKEN=your_token_here
    
      # optional settings
      - LOG_CHANNEL_ID=channel_to_send_working_log
      - ERROR_LOG_CHANNEL_ID=channel_to_send_error_log
    networks:
      - dockge_default
    dns:
      - 8.8.8.8
      - 1.1.1.1
networks:
  dockge_default:
    external: true

```