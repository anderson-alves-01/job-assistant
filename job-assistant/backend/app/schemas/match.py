from pydantic import BaseModel

from app.schemas.job import JobResponse


class JobMatchResponse(BaseModel):
    """
    Resultado da comparação entre uma vaga e o perfil.
    """

    job: JobResponse

    total_score: int
    recommendation: str

    title_score: int
    skills_score: int
    location_score: int
    seniority_score: int
    employment_type_score: int

    matched_primary_skills: list[str]
    matched_secondary_skills: list[str]
    missing_primary_skills: list[str]

    rejection_reasons: list[str]
    summary: str