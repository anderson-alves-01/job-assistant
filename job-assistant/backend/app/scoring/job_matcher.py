import re
import unicodedata

from app.models.job import Job
from app.schemas.job import JobResponse
from app.schemas.match import JobMatchResponse


class JobMatcher:
    """
    Compara uma vaga com o perfil profissional do candidato.
    """

    SKILL_SYNONYMS = {
        "Java": [
            "java",
            "java 8",
            "java 11",
            "java 17",
            "java 21",
            "jvm",
        ],
        "Spring Boot": [
            "spring boot",
            "springboot",
            "spring framework",
        ],
        "Microservices": [
            "microservices",
            "microservice",
            "distributed systems",
            "distributed architecture",
        ],
        "AWS": [
            "aws",
            "amazon web services",
            "lambda",
            "eks",
            "ecs",
            "s3",
            "rds",
            "dynamodb",
            "sqs",
            "sns",
            "cloudwatch",
        ],
        "REST API": [
            "rest api",
            "rest apis",
            "restful",
        ],
        "PostgreSQL": [
            "postgresql",
            "postgres",
        ],
        "Kafka": [
            "kafka",
            "apache kafka",
            "event streaming",
        ],
        "Docker": [
            "docker",
            "docker compose",
            "containerization",
        ],
        "Kubernetes": [
            "kubernetes",
            "k8s",
        ],
        "Redis": [
            "redis",
            "redis cache",
        ],
        "MongoDB": [
            "mongodb",
            "mongo db",
            "nosql database",
        ],
        "Azure": [
            "azure",
            "azure functions",
            "azure kubernetes",
        ],
        "GCP": [
            "gcp",
            "google cloud",
            "google cloud platform",
        ],
        "Terraform": [
            "terraform",
            "iac",
            "infrastructure as code",
        ],
        "GitHub Actions": [
            "github actions",
            "github workflows",
            "ci cd",
            "ci/cd",
        ],
        "DDD": [
            "ddd",
            "domain driven design",
            "domain-driven design",
        ],
        "Hexagonal Architecture": [
            "hexagonal architecture",
            "ports and adapters",
        ],
        "Clean Architecture": [
            "clean architecture",
        ],
        "CQRS": [
            "cqrs",
        ],
        "SAGA": [
            "saga",
            "saga pattern",
        ],
        "Event-driven architecture": [
            "event driven",
            "event-driven",
            "event driven architecture",
            "eda",
        ],
    }

    def __init__(self, profile: dict):
        self.profile = profile

        self.target = profile.get(
            "target",
            {},
        )

        self.skills = profile.get(
            "skills",
            {},
        )

        self.experience = profile.get(
            "experience",
            {},
        )

        self.exclusions = profile.get(
            "exclusions",
            {},
        )

    def match(self, job: Job) -> JobMatchResponse:
        """
        Calcula aderência de uma vaga ao perfil.
        """

        corpus = self._build_corpus(job)

        rejection_reasons = self._get_rejection_reasons(
            job=job,
            corpus=corpus,
        )

        title_score = self._score_title(job)
        skills_result = self._score_skills(corpus)
        location_score = self._score_location(job, corpus)
        seniority_score = self._score_seniority(corpus)
        employment_type_score = self._score_employment_type(job)

        total_score = (
            title_score
            + skills_result["score"]
            + location_score
            + seniority_score
            + employment_type_score
        )

        total_score = min(
            total_score,
            100,
        )

        if rejection_reasons:
            recommendation = "DESCARTAR"
            total_score = min(
                total_score,
                50,
            )

        elif total_score >= 80:
            recommendation = "CANDIDATAR"

        elif total_score >= 60:
            recommendation = "AVALIAR"

        else:
            recommendation = "DESCARTAR"

        summary = self._build_summary(
            total_score=total_score,
            recommendation=recommendation,
            matched_primary=skills_result["matched_primary"],
            missing_primary=skills_result["missing_primary"],
            rejection_reasons=rejection_reasons,
        )

        return JobMatchResponse(
            job=JobResponse.model_validate(job),
            total_score=total_score,
            recommendation=recommendation,
            title_score=title_score,
            skills_score=skills_result["score"],
            location_score=location_score,
            seniority_score=seniority_score,
            employment_type_score=employment_type_score,
            matched_primary_skills=skills_result["matched_primary"],
            matched_secondary_skills=skills_result["matched_secondary"],
            missing_primary_skills=skills_result["missing_primary"],
            rejection_reasons=rejection_reasons,
            summary=summary,
        )

    def _build_corpus(self, job: Job) -> str:
        """
        Junta título, descrição, empresa, localização e tipo de contrato.
        """

        values = [
            job.title,
            job.company,
            job.category,
            job.description,
            job.location,
            job.employment_type,
            job.salary_text,
        ]

        return self._normalize_text(
            " ".join(
                value or ""
                for value in values
            )
        )

    def _score_title(self, job: Job) -> int:
        """
        Pontuação de cargo desejado.
        Peso máximo: 20.
        """

        title = self._normalize_text(job.title)

        target_roles = self.target.get(
            "roles",
            [],
        )

        for role in target_roles:
            normalized_role = self._normalize_text(role)

            if normalized_role in title:
                return 20

        role_keywords = [
            "senior software engineer",
            "senior java",
            "java developer",
            "backend engineer",
            "backend developer",
            "software architect",
            "solutions architect",
            "tech lead",
            "technical lead",
            "lead engineer",
        ]

        for keyword in role_keywords:
            if keyword in title:
                return 18

        if "java" in title:
            return 14

        if "backend" in title:
            return 12

        if "software engineer" in title:
            return 12

        if "developer" in title:
            return 8

        return 0

    def _score_skills(self, corpus: str) -> dict:
        """
        Pontuação de competências.
        Peso máximo: 40.

        Primary skills: até 30 pontos.
        Secondary + architecture: até 10 pontos.
        """

        primary_skills = self.skills.get(
            "primary",
            [],
        )

        secondary_skills = (
            self.skills.get(
                "secondary",
                [],
            )
            + self.skills.get(
                "architecture",
                [],
            )
        )

        matched_primary = self._find_skills(
            skills=primary_skills,
            corpus=corpus,
        )

        matched_secondary = self._find_skills(
            skills=secondary_skills,
            corpus=corpus,
        )

        missing_primary = [
            skill
            for skill in primary_skills
            if skill not in matched_primary
        ]

        primary_score = 0

        if primary_skills:
            primary_score = round(
                30
                * len(matched_primary)
                / len(primary_skills)
            )

        secondary_score = min(
            len(matched_secondary) * 2,
            10,
        )

        return {
            "score": primary_score + secondary_score,
            "matched_primary": matched_primary,
            "matched_secondary": matched_secondary,
            "missing_primary": missing_primary,
        }

    def _score_location(
        self,
        job: Job,
        corpus: str,
    ) -> int:
        """
        Pontuação de localização/modalidade.
        Peso máximo: 20.
        """

        location = self._normalize_text(
            job.location or ""
        )

        positive_terms = [
            "remote",
            "worldwide",
            "anywhere",
            "latin america",
            "latam",
            "americas",
            "brazil",
            "brasil",
            "south america",
            "global",
        ]

        for term in positive_terms:
            if term in location or term in corpus:
                return 20

        work_modes = self.target.get(
            "work_modes",
            [],
        )

        normalized_work_modes = [
            self._normalize_text(mode)
            for mode in work_modes
        ]

        if "remote" in normalized_work_modes:
            if not location:
                return 12

        return 5

    def _score_seniority(self, corpus: str) -> int:
        """
        Pontuação de senioridade.
        Peso máximo: 10.
        """

        seniority_terms = [
            "senior",
            "sr",
            "lead",
            "principal",
            "staff",
            "architect",
            "specialist",
        ]

        for term in seniority_terms:
            if self._contains_word(corpus, term):
                return 10

        if self._contains_word(corpus, "mid"):
            return 4

        return 6

    def _score_employment_type(self, job: Job) -> int:
        """
        Pontuação de tipo de contratação.
        Peso máximo: 10.
        """

        employment_type = self._normalize_text(
            job.employment_type or ""
        )

        if not employment_type:
            return 5

        accepted_types = self.target.get(
            "employment_types",
            [],
        )

        for accepted_type in accepted_types:
            normalized_type = self._normalize_text(
                accepted_type
            )

            if normalized_type in employment_type:
                return 10

        positive_terms = [
            "full time",
            "contract",
            "contractor",
            "freelance",
            "pj",
            "clt",
        ]

        for term in positive_terms:
            if term in employment_type:
                return 8

        return 4

    def _get_rejection_reasons(
        self,
        job: Job,
        corpus: str,
    ) -> list[str]:
        """
        Identifica motivos objetivos para descartar.
        """

        reasons: list[str] = []

        title = self._normalize_text(job.title)
        location = self._normalize_text(
            job.location or ""
        )

        excluded_roles = self.exclusions.get(
            "roles",
            [],
        )

        for role in excluded_roles:
            normalized_role = self._normalize_text(role)

            if self._contains_word(title, normalized_role):
                reasons.append(
                    f"Cargo excluído pelo perfil: {role}"
                )

        restricted_location_patterns = [
            "us only",
            "usa only",
            "united states only",
            "only us",
            "only usa",
            "must be located in the us",
            "must be based in the us",
            "us based only",
        ]

        for pattern in restricted_location_patterns:
            if pattern in location or pattern in corpus:
                reasons.append(
                    "Vaga aparentemente restrita aos EUA."
                )

                break

        if "intern" in title or "internship" in title:
            reasons.append(
                "Vaga de estágio/internship."
            )

        if "trainee" in title:
            reasons.append(
                "Vaga de trainee."
            )

        if "junior" in title or self._contains_word(title, "jr"):
            reasons.append(
                "Vaga júnior."
            )

        return reasons

    def _find_skills(
        self,
        skills: list[str],
        corpus: str,
    ) -> list[str]:
        """
        Localiza skills no texto da vaga.
        """

        matched: list[str] = []

        for skill in skills:
            variants = self.SKILL_SYNONYMS.get(
                skill,
                [skill],
            )

            for variant in variants:
                if self._contains_skill_variant(
                    corpus,
                    variant,
                ):
                    matched.append(skill)
                    break

        return matched

    @staticmethod
    def _contains_skill_variant(
        corpus: str,
        variant: str,
    ) -> bool:
        """
        Verifica presença de uma skill sem considerar substrings de outras palavras.
        """

        normalized_variant = JobMatcher._normalize_text(variant)
        if not normalized_variant:
            return False

        if normalized_variant in corpus:
            return True

        pattern = rf"(?<![a-z0-9]){re.escape(normalized_variant)}(?![a-z0-9])"
        return bool(re.search(pattern, corpus))

    def _build_summary(
        self,
        total_score: int,
        recommendation: str,
        matched_primary: list[str],
        missing_primary: list[str],
        rejection_reasons: list[str],
    ) -> str:
        """
        Cria um resumo curto da avaliação.
        """

        if rejection_reasons:
            return (
                f"Score {total_score}. Recomendação: {recommendation}. "
                f"Motivos de descarte: {'; '.join(rejection_reasons)}"
            )

        if recommendation == "CANDIDATAR":
            return (
                f"Score {total_score}. Boa aderência ao perfil. "
                f"Skills principais encontradas: "
                f"{', '.join(matched_primary) or 'nenhuma'}."
            )

        if recommendation == "AVALIAR":
            return (
                f"Score {total_score}. A vaga tem alguma aderência, "
                f"mas exige revisão manual. Skills principais ausentes: "
                f"{', '.join(missing_primary) or 'nenhuma'}."
            )

        return (
            f"Score {total_score}. Baixa aderência ao perfil. "
            f"Skills principais ausentes: "
            f"{', '.join(missing_primary) or 'nenhuma'}."
        )

    @staticmethod
    def _normalize_text(value: str) -> str:
        """
        Normaliza texto para comparação.
        """

        value = unicodedata.normalize(
            "NFKD",
            value,
        )

        value = "".join(
            char
            for char in value
            if not unicodedata.combining(char)
        )

        value = value.lower()

        value = re.sub(
            r"[^a-z0-9+#/.]+",
            " ",
            value,
        )

        return " ".join(
            value.split()
        )

    @staticmethod
    def _contains_word(
        text: str,
        word: str,
    ) -> bool:
        """
        Verifica presença de palavra isolada.
        """

        escaped_word = re.escape(word)

        return bool(
            re.search(
                rf"\b{escaped_word}\b",
                text,
            )
        )