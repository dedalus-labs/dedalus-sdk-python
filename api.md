# Root

Types:

```python
from dedalus_labs.types import RootGetResponse
```

Methods:

- <code title="get /">client.root.<a href="./src/dedalus_labs/resources/root.py">get</a>() -> <a href="./src/dedalus_labs/types/root_get_response.py">RootGetResponse</a></code>

# Health

Types:

```python
from dedalus_labs.types import HealthCheckResponse
```

Methods:

- <code title="get /health">client.health.<a href="./src/dedalus_labs/resources/health.py">check</a>() -> <a href="./src/dedalus_labs/types/health_check_response.py">HealthCheckResponse</a></code>

# Models

Types:

```python
from dedalus_labs.types import ModelsResponse, ModelRetrieveResponse
```

Methods:

- <code title="get /v1/models/{model_id}">client.models.<a href="./src/dedalus_labs/resources/models.py">retrieve</a>(model_id) -> <a href="./src/dedalus_labs/types/model_retrieve_response.py">ModelRetrieveResponse</a></code>
- <code title="get /v1/models">client.models.<a href="./src/dedalus_labs/resources/models.py">list</a>() -> <a href="./src/dedalus_labs/types/models_response.py">ModelsResponse</a></code>

# Chat

## Completions

Types:

```python
from dedalus_labs.types.chat import (
    ChatCompletionTokenLogprob,
    Completion,
    CompletionRequest,
    TopLogprob,
)
```
