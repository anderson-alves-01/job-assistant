from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.job_repository import JobRepository
from app.schemas.job import (
    CollectionResponse,
    JobResponse,
)
from app.schemas.match import JobMatchResponse
from app.scoring.job_matcher import JobMatcher
from app.services.job_collection import JobCollectionService
from app.services.profile_service import load_profile


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "/collect/remotive",
    response_model=CollectionResponse,
)
async def collect_remotive_jobs(
    limit: int = Query(
        default=20,
        ge=1,
        le=200,
    ),
    db: Session = Depends(get_db),
) -> CollectionResponse:
    """
    Busca vagas da Remotive e salva no banco.
    """

    service = JobCollectionService(db)

    try:
        return await service.collect_remotive(
            limit=limit
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "Não foi possível coletar "
                f"as vagas da Remotive: {exc}"
            ),
        ) from exc


@router.get(
    "",
    response_model=list[JobResponse],
)
def list_jobs(
    source: str | None = None,
    search: str | None = None,
    status: str | None = None,
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
    ),
    db: Session = Depends(get_db),
) -> list[JobResponse]:
    """
    Lista vagas armazenadas no banco.
    """

    repository = JobRepository(db)

    return repository.list_jobs(
        source=source,
        search=search,
        status=status,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/matches",
    response_model=list[JobMatchResponse],
)
def list_job_matches(
    source: str | None = None,
    search: str | None = None,
    status: str | None = None,
    min_score: int = Query(
        default=0,
        ge=0,
        le=100,
    ),
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
    ),
    db: Session = Depends(get_db),
) -> list[JobMatchResponse]:
    """
    Lista vagas com score de aderência ao perfil.
    """

    repository = JobRepository(db)

    jobs = repository.list_jobs(
        source=source,
        search=search,
        status=status,
        skip=skip,
        limit=limit,
    )

    profile = load_profile()
    matcher = JobMatcher(profile)

    matches = [
        matcher.match(job)
        for job in jobs
    ]

    filtered_matches = [
        match
        for match in matches
        if match.total_score >= min_score
    ]

    return sorted(
        filtered_matches,
        key=lambda item: item.total_score,
        reverse=True,
    )


@router.get(
    "/{job_id}/match",
    response_model=JobMatchResponse,
)
def get_job_match(
    job_id: int,
    db: Session = Depends(get_db),
) -> JobMatchResponse:
    """
    Calcula a aderência de uma vaga específica.
    """

    repository = JobRepository(db)

    job = repository.get_by_id(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Vaga não encontrada",
        )

    profile = load_profile()
    matcher = JobMatcher(profile)

    return matcher.match(job)


@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
) -> JobResponse:
    """
    Consulta os detalhes de uma vaga.
    """

    repository = JobRepository(db)

    job = repository.get_by_id(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Vaga não encontrada",
        )

    return job