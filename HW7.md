# HW 7 Применение In-Memory СУБД

### Общая информация
Модуль диалогов вынесен в In-Memory СУБД (TARANTOOL).

Логика вынесена в функцию send_message(отправка сообщения) и get_conversation (получение диалога), в файле messages-service\tarantool\init.lua

В качестве БД используется TARANTOOL


### Нагрузочное тестирвоание



[send_message]: 
1000 запросов на запись, 50 параллельно

- Citus (PostgreSQL)

Total time: 7.81s

RPS: 128.07

Avg latency: 271.39ms


- TARANTOOL

Total time: 2.09s

RPS: 479.58

Avg latency: 64.45ms

[get_conversation]: 
1000 запросов на чтение, 50 параллельно

- Citus (PostgreSQL)

Total time: 5.84s

RPS: 171.29

Avg latency: 172.55ms


- TARANTOOL

Total time: 2.27s

RPS: 440.71

Avg latency: 65.78ms
