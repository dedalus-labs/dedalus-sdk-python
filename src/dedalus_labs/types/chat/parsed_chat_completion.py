"""ParsedChatCompletion type stub.

Placeholder for type hinting. Actual parsing returns modified Completion object.
"""

from __future__ import annotations

from .completion import Completion

# For now, ParsedChatCompletion is just an alias
# The parse_chat_completion function adds .parsed attribute dynamically
ParsedChatCompletion = Completion
