import hashlib
import re
from datetime import UTC, datetime

import httpx
from bs4 import BeautifulSoup

from app.connectors.base import JobConnector
from app.schemas.job import NormalizedJob


class RemotiveConnector(JobConnector):
    """
    Conector responsável por buscar vagas da Remotive.
    """

    BASE_URL = "https://remotive.com/api/remote-jobs"

    @property
    def source_name(self) -> str:
        return "REMOTIVE"

    async def fetch_jobs(
        self,
        limit: int = 100,
    ) -> list[NormalizedJob]:
        """
        Busca vagas de desenvolvimento de software.
        """

        params = {
            "category": "software-dev",
            "limit": limit,
        }

        headers = {
            "Accept": "application/json",
            "User-Agent": "JobApplicationAssistant/0.1",
        }

        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers=headers,
        ) as client:
            response = await client.get(
                self.BASE_URL,
                params=params,
            )

            response.raise_for_status()
            payload = response.json()

        normalized_jobs: list[NormalizedJob] = []

        for raw_job in payload.get("jobs", []):
            try:
                normalized_job = self._normalize(
                    raw_job
                )

                normalized_jobs.append(
                    normalized_job
                )

            except (
                KeyError,
                ValueError,
                TypeError,
            ):
                # Uma vaga inválida não interrompe toda a coleta.
                continue

        return normalized_jobs

    def _normalize(
        self,
        raw_job: dict,
    ) -> NormalizedJob:
        """
        Converte o formato recebido da Remotive
        para o formato padrão do sistema.
        """

        external_id = raw_job.get("id")

        if external_id is None:
            raise ValueError(
                "Remotive job without id"
            )

        title = self._clean_text(
            raw_job.get("title")
        )

        if not title:
            raise ValueError(
                "Remotive job without title"
            )

        company = self._clean_text(
            raw_job.get("company_name")
        )

        location = self._clean_text(
            raw_job.get(
                "candidate_required_location"
            )
        )

        description = self._html_to_text(
            raw_job.get("description", "")
        )

        source_url = self._clean_text(
            raw_job.get("url")
        )

        if not source_url:
            raise ValueError(
                "Remotive job without url"
            )

        content_hash = self._create_content_hash(
            title=title,
            company=company or "",
            location=location or "",
        )

        return NormalizedJob(
            source=self.source_name,
            external_id=str(external_id),
            title=title,
            company=company,
            category=self._clean_text(
                raw_job.get("category")
            ),
            description=description,
            location=location,
            employment_type=self._clean_text(
                raw_job.get("job_type")
            ),
            salary_text=self._clean_text(
                raw_job.get("salary")
            ),
            application_url=source_url,
            source_url=source_url,
            published_at=self._parse_datetime(
                raw_job.get(
                    "publication_date"
                )
            ),
            content_hash=content_hash,
        )

    @staticmethod
    def _html_to_text(
        value: str,
    ) -> str:
        """
        Remove HTML da descrição da vaga.
        """

        soup = BeautifulSoup(
            value or "",
            "html.parser",
        )

        text = soup.get_text(
            " ",
            strip=True,
        )

        return " ".join(
            text.split()
        )

    @staticmethod
    def _clean_text(
        value: object,
    ) -> str | None:
        """
        Converte o valor para texto e remove
        espaços duplicados.
        """

        if value is None:
            return None

        cleaned = " ".join(
            str(value).strip().split()
        )

        return cleaned or None

    @staticmethod
    def _parse_datetime(
        value: str | None,
    ) -> datetime | None:
        """
        Converte a data ISO recebida pela API.
        """

        if not value:
            return None

        normalized_value = value.replace(
            "Z",
            "+00:00",
        )

        parsed = datetime.fromisoformat(
            normalized_value
        )

        if parsed.tzinfo is None:
            parsed = parsed.replace(
                tzinfo=UTC
            )

        return parsed

    @staticmethod
    def _normalize_hash_text(
        value: str,
    ) -> str:
        """
        Normaliza o texto antes da criação do hash.
        """

        value = value.lower().strip()

        value = re.sub(
            r"[^a-z0-9]+",
            " ",
            value,
        )

        return " ".join(
            value.split()
        )

    def _create_content_hash(
        self,
        title: str,
        company: str,
        location: str,
    ) -> str:
        """
        Cria uma assinatura da vaga.

        Isso ajudará posteriormente na detecção
        de duplicidades entre sites diferentes.
        """

        normalized_content = "|".join(
            [
                self._normalize_hash_text(
                    title
                ),
                self._normalize_hash_text(
                    company
                ),
                self._normalize_hash_text(
                    location
                ),
            ]
        )

        return hashlib.sha256(
            normalized_content.encode(
                "utf-8"
            )
        ).hexdigest()