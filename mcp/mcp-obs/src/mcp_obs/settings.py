"""Settings for the Observability MCP server."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    victorialogs_url: str = Field(
        default="http://victorialogs:9428",
        validation_alias="NANOBOT_VICTORIALOGS_URL",
    )
    victoriatraces_url: str = Field(
        default="http://victoriatraces:10428",
        validation_alias="NANOBOT_VICTORIATRACES_URL",
    )
