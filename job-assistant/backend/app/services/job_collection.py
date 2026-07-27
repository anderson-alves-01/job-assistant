from sqlalchemy.orm import Session

from app.connectors.remotive import RemotiveConnector
from app.repositories.job_repository import JobRepository
from app.schemas.job import CollectionResponse


class JobCollectionService:
    """
    Serviço responsável pela coleta e persistência.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db
        self.repository = JobRepository(
            db
        )

    async def collect_remotive(
        self,
        limit: int,
    ) -> CollectionResponse:
        """
        Busca vagas na Remotive e salva no PostgreSQL.
        """

        connector = RemotiveConnector()

        jobs = await connector.fetch_jobs(
            limit=limit
        )

        inserted = 0
        updated = 0

        try:
            for job in jobs:
                operation = (
                    self.repository.upsert(
                        job
                    )
                )

                if operation == "inserted":
                    inserted += 1
                else:
                    updated += 1

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

        return CollectionResponse(
            source=connector.source_name,
            received=len(jobs),
            inserted=inserted,
            updated=updated,
        )