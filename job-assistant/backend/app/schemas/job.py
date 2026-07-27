from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NormalizedJob(BaseModel):
    """
    Formato padrão interno de uma vaga.

    Todos os conectores convertem seus dados
    para este modelo antes da persistência.
    """

    source: str
    external_id: str
    title: str
    company: str | None = None
    category: str | None = None
    description: str
    location: str | None = None
    employment_type: str | None = None
    salary_text: str | None = None
    application_url: str
    source_url: str
    published_at: datetime | None = None
    content_hash: str


class JobResponse(BaseModel):
    """
    Modelo retornado pelos endpoints da API.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    source: str
    external_id: str
    title: str
    company: str | None
    category: str | None
    description: str
    location: str | None
    employment_type: str | None
    salary_text: str | None
    application_url: str
    source_url: str
    published_at: datetime | None
    content_hash: str
    status: str
    collected_at: datetime
    updated_at: datetime


class CollectionResponse(BaseModel):
    """
    Resultado resumido de uma coleta.
    """

    source: str

    received: int = Field(
        ge=0,
        description="Quantidade recebida da fonte",
    )

    inserted: int = Field(
        ge=0,
        description="Quantidade de vagas inseridas",
    )

    updated: int = Field(
        ge=0,
        description="Quantidade de vagas atualizadas",
    )