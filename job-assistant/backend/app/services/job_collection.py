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
        Busca vagas na Remotive e sincroniza o banco local.
        """

        connector = RemotiveConnector()

        jobs = await connector.fetch_jobs(
            limit=limit
        )

        try:
            sync_result = self.repository.sync_jobs(
                source=connector.source_name,
                incoming_jobs=jobs,
            )
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        return CollectionResponse(
            source=connector.source_name,
            received=len(jobs),
            inserted=sync_result["inserted"],
            updated=sync_result["updated"],
            removed=sync_result["removed"],
        )