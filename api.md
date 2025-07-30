# DedalusSDK

Types:

```python
from dedalus_sdk.types import GetRootResponse
```

Methods:

- <code title="get /">client.<a href="./src/dedalus_sdk/_client.py">get_root</a>() -> <a href="./src/dedalus_sdk/types/get_root_response.py">GetRootResponse</a></code>

# Health

Types:

```python
from dedalus_sdk.types import HealthCheckResponse
```

Methods:

- <code title="get /health">client.health.<a href="./src/dedalus_sdk/resources/health.py">check</a>() -> <a href="./src/dedalus_sdk/types/health_check_response.py">HealthCheckResponse</a></code>

# Models

Types:

```python
from dedalus_sdk.types import Model, ModelListResponse
```

Methods:

- <code title="get /v1/models/{model_id}">client.models.<a href="./src/dedalus_sdk/resources/models.py">retrieve</a>(model_id) -> <a href="./src/dedalus_sdk/types/model.py">Model</a></code>
- <code title="get /v1/models">client.models.<a href="./src/dedalus_sdk/resources/models.py">list</a>() -> <a href="./src/dedalus_sdk/types/model_list_response.py">ModelListResponse</a></code>

# Chat

Types:

```python
from dedalus_sdk.types import ChatCompletionTokenLogprob, ChatCreateResponse
```

Methods:

- <code title="post /v1/chat">client.chat.<a href="./src/dedalus_sdk/resources/chat.py">create</a>(\*\*<a href="src/dedalus_sdk/types/chat_create_params.py">params</a>) -> <a href="./src/dedalus_sdk/types/chat_create_response.py">ChatCreateResponse</a></code>
