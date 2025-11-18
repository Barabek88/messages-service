# HW 5 Шардирование

### Общая информация
Создан сервис сообщений: messages-service

В качестве БД используется PG с EXTENSION citus

Один координатор - citus-coordinator
2 worker'а: citus-worker1, citus-worker2

Docker file: messages-service\docker-compose.yml

Структура таблицы сообщений

CREATE TABLE messages (
    id UUID DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL,
    sender_id UUID NOT NULL,
    receiver_id UUID NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active boolean DEFAULT true,
    PRIMARY KEY (conversation_id, id)
);

В качестве ключа шардирования выбрано поле ID диалога - conversation_id

SELECT create_distributed_table('messages', 'conversation_id');

conversation_id вычисляется на основе ID участников диалога

def get_conversation_id(user1_id: PyUUID, user2_id: PyUUID) -> PyUUID:
    ids = sorted([str(user1_id), str(user2_id)])
    return uuid5(NAMESPACE_DNS, f"{ids[0]}:{ids[1]}")


Таким образом, вся переписка между двумя участниками будет храниться на одном шарде, что ускоряет доступ к сообщениям.


### Решардинг

Citus  поддерживает автоматический решардинг без даунтайма

- Добавляем worker к координатору SELECT citus_add_node
- После чего ребалансируем таблицу SELECT rebalance_table_shards(:table)

messages-service\app\controllers\citus_resharding_controller.py

messages-service\app\services\citus_resharding_service.py

