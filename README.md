# FastAPI Jira Action API

## How to create Jira API Token

## API List

* PingPong과 같이 Payload 필요없는 API가 아니라면 Get Method를 사용하지 않는다.
    * Payload 전달을 위해서...
* Get API가 필요한경우 list 혹은 one을 마지막에 추가하도록 한다.
* http://localhost:9000/docs
* http://localhost:9000/redoc

![img.png](docs/.image/api_list.png)

## Docker

```shell
docker build -t fastapi-jira-action .
docker run -d -p 9010:9000 fastapi-jira-action
```

### Ref.

* https://fastapi.tiangolo.com/