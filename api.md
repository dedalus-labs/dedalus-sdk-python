# Shared Types

```python
from dedalus_labs.types import (
    DedalusModel,
    DedalusModelChoice,
    ResponseFormatJSONObject,
    ResponseFormatJSONSchema,
    ResponseFormatText,
)
```

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
from dedalus_labs.types import ListModelsResponse, Model
```

Methods:

- <code title="get /v1/models/{model_id}">client.models.<a href="./src/dedalus_labs/resources/models.py">retrieve</a>(model_id) -> <a href="./src/dedalus_labs/types/model.py">Model</a></code>
- <code title="get /v1/models">client.models.<a href="./src/dedalus_labs/resources/models.py">list</a>() -> <a href="./src/dedalus_labs/types/list_models_response.py">ListModelsResponse</a></code>

# Embeddings

Types:

```python
from dedalus_labs.types import CreateEmbeddingRequest, CreateEmbeddingResponse
```

Methods:

- <code title="post /v1/embeddings">client.embeddings.<a href="./src/dedalus_labs/resources/embeddings.py">create</a>(\*\*<a href="src/dedalus_labs/types/embedding_create_params.py">params</a>) -> <a href="./src/dedalus_labs/types/create_embedding_response.py">CreateEmbeddingResponse</a></code>

# Audio

## Speech

Methods:

- <code title="post /v1/audio/speech">client.audio.speech.<a href="./src/dedalus_labs/resources/audio/speech.py">create</a>(\*\*<a href="src/dedalus_labs/types/audio/speech_create_params.py">params</a>) -> BinaryAPIResponse</code>

## Transcriptions

Types:

```python
from dedalus_labs.types.audio import TranscriptionCreateResponse
```

Methods:

- <code title="post /v1/audio/transcriptions">client.audio.transcriptions.<a href="./src/dedalus_labs/resources/audio/transcriptions.py">create</a>(\*\*<a href="src/dedalus_labs/types/audio/transcription_create_params.py">params</a>) -> <a href="./src/dedalus_labs/types/audio/transcription_create_response.py">TranscriptionCreateResponse</a></code>

## Translations

Types:

```python
from dedalus_labs.types.audio import TranslationCreateResponse
```

Methods:

- <code title="post /v1/audio/translations">client.audio.translations.<a href="./src/dedalus_labs/resources/audio/translations.py">create</a>(\*\*<a href="src/dedalus_labs/types/audio/translation_create_params.py">params</a>) -> <a href="./src/dedalus_labs/types/audio/translation_create_response.py">TranslationCreateResponse</a></code>

# Images

Types:

```python
from dedalus_labs.types import CreateImageRequest, Image, ImagesResponse
```

Methods:

- <code title="post /v1/images/variations">client.images.<a href="./src/dedalus_labs/resources/images.py">create_variation</a>(\*\*<a href="src/dedalus_labs/types/image_create_variation_params.py">params</a>) -> <a href="./src/dedalus_labs/types/images_response.py">ImagesResponse</a></code>
- <code title="post /v1/images/edits">client.images.<a href="./src/dedalus_labs/resources/images.py">edit</a>(\*\*<a href="src/dedalus_labs/types/image_edit_params.py">params</a>) -> <a href="./src/dedalus_labs/types/images_response.py">ImagesResponse</a></code>
- <code title="post /v1/images/generations">client.images.<a href="./src/dedalus_labs/resources/images.py">generate</a>(\*\*<a href="src/dedalus_labs/types/image_generate_params.py">params</a>) -> <a href="./src/dedalus_labs/types/images_response.py">ImagesResponse</a></code>

# Chat

## Completions

Types:

```python
from dedalus_labs.types.chat import (
    ChatCompletionTokenLogprob,
    Completion,
    CompletionRequest,
    ModelID,
    Models,
    StreamChunk,
    TopLogprob,
)
```

Methods:

- <code title="post /v1/chat/completions">client.chat.completions.<a href="./src/dedalus_labs/resources/chat/completions.py">create</a>(\*\*<a href="src/dedalus_labs/types/chat/completion_create_params.py">params</a>) -> <a href="./src/dedalus_labs/types/chat/completion.py">Completion</a></code>
