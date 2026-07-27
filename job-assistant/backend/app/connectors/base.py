from abc import ABC, abstractmethod

from app.schemas.job import NormalizedJob


class JobConnector(ABC):
    """
    Interface comum para todos os sites de vagas.
    """

    @property
    @abstractmethod
    def source_name(self) -> str:
        """
        Nome interno da fonte.
        """

        raise NotImplementedError

    @abstractmethod
    async def fetch_jobs(
        self,
        limit: int = 100,
    ) -> list[NormalizedJob]:
        """
        Busca e normaliza vagas da fonte.
        """

        raise NotImplementedError