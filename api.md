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
from dedalus_labs.types import DedalusModel, Model, ModelsResponse
```

Methods:

- <code title="get /v1/models/{model_id}">client.models.<a href="./src/dedalus_labs/resources/models.py">retrieve</a>(model_id) -> <a href="./src/dedalus_labs/types/dedalus_model.py">DedalusModel</a></code>
- <code title="get /v1/models">client.models.<a href="./src/dedalus_labs/resources/models.py">list</a>() -> <a href="./src/dedalus_labs/types/models_response.py">ModelsResponse</a></code>

# Chat

## Completions

Types:

```python
from dedalus_labs.types.chat import (
    ChatCompletionTokenLogprob,
    Completion,
    CompletionRequestMessages,
    DedalusModelChoice,
    ModelID,
    Models,
    StreamChunk,
    TopLogprob,
)
```

Methods:

- <code title="post /v1/chat/completions">client.chat.completions.<a href="./src/dedalus_labs/resources/chat/completions.py">create</a>(\*\*<a href="src/dedalus_labs/types/chat/completion_create_params.py">params</a>) -> <a href="./src/dedalus_labs/types/chat/stream_chunk.py">StreamChunk</a></code>
