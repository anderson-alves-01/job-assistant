
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.schemas.job import NormalizedJob


class JobRepository:
    """
    Repositório responsável pelas operações de banco
    relacionadas às vagas.
    """

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: NormalizedJob) -> str:
        """
        Insere uma vaga nova ou atualiza uma vaga existente.

        A vaga é identificada inicialmente pela combinação:
        source + external_id.
        """

        statement = select(Job).where(
            Job.source == data.source,
            Job.external_id == data.external_id,
        )

        existing_job = self.db.scalar(statement)

        job_data = data.model_dump()

        if existing_job is None:
            new_job = Job(**job_data)
            self.db.add(new_job)

            return "inserted"

        for field_name, field_value in job_data.items():
            setattr(
                existing_job,
                field_name,
                field_value,
            )

        return "updated"

    def sync_jobs(
        self,
        source: str,
        incoming_jobs: list[NormalizedJob],
    ) -> dict[str, int]:
        """
        Sincroniza a base local com a fonte atual, removendo vagas
        que não estiveram mais presentes na última coleta.
        """

        incoming_ids = {
            (source.upper(), job.external_id)
            for job in incoming_jobs
        }

        existing_jobs = self.db.scalars(
            select(Job).where(Job.source == source.upper())
        ).all()

        existing_ids = {
            (job.source, job.external_id)
            for job in existing_jobs
        }

        inserted = 0
        updated = 0
        removed = 0

        for job in incoming_jobs:
            operation = self.upsert(job)
            if operation == "inserted":
                inserted += 1
            else:
                updated += 1

        stale_jobs = [
            job
            for job in existing_jobs
            if (job.source, job.external_id) not in incoming_ids
        ]

        for stale_job in stale_jobs:
            self.db.delete(stale_job)
            removed += 1

        return {
            "inserted": inserted,
            "updated": updated,
            "removed": removed,
        }

    def list_jobs(
        self,
        source: str | None = None,
        search: str | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Job]:
        """
        Lista vagas armazenadas com filtros opcionais.
        """

        statement = select(Job)

        if source:
            statement = statement.where(
                Job.source == source.upper()
            )

        if status:
            normalized_status = status.upper()
            if normalized_status == "ALL":
                pass
            else:
                statement = statement.where(
                    Job.status == normalized_status
                )
        else:
            statement = statement.where(
                Job.status != "ARCHIVED"
            )

        if search:
            cleaned_search = search.strip()

            if cleaned_search:
                pattern = f"%{cleaned_search}%"

                statement = statement.where(
                    or_(
                        Job.title.ilike(pattern),
                        Job.company.ilike(pattern),
                        Job.description.ilike(pattern),
                        Job.category.ilike(pattern),
                    )
                )

        statement = (
            statement
            .order_by(
                Job.published_at.desc().nullslast(),
                Job.id.desc(),
            )
            .offset(skip)
            .limit(limit)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_id(self, job_id: int) -> Job | None:
        """
        Retorna uma vaga pelo ID interno.
        """

        return self.db.get(
            Job,
            job_id,
        )