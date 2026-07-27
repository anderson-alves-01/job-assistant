import json

from app.core.settings import settings


def load_profile() -> dict:
    """
    Carrega o perfil profissional salvo em profile/profile.json.
    """

    if not settings.profile_path.exists():
        raise FileNotFoundError(
            f"Profile file not found: {settings.profile_path}"
        )

    with settings.profile_path.open(
        "r",
        encoding="utf-8",
    ) as profile_file:
        return json.load(profile_file)