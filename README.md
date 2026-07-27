# Job Application Assistant

Assistente local para busca, triagem e preenchimento assistido de candidaturas a vagas remotas.

O objetivo do projeto é reduzir o trabalho manual de procurar vagas em múltiplas plataformas, comparar cada oportunidade com um perfil profissional previamente configurado e preparar o preenchimento de candidaturas sem acionar o envio automático.

Este MVP segue o modelo **Nível 2 — Preenchimento Assistido**: o sistema coleta e avalia vagas, organiza os resultados e futuramente ajudará a preencher formulários, mas a decisão final e o clique em “Enviar” continuam sob controle do usuário.

---

## 1. Visão geral

O projeto foi pensado para funcionar em etapas:

1. Cadastrar um perfil profissional estruturado.
2. Buscar vagas em fontes públicas ou conectores controlados.
3. Normalizar as vagas em um formato único.
4. Salvar as vagas no PostgreSQL.
5. Evitar duplicidade por fonte e identificador externo.
6. Calcular aderência entre vaga e perfil profissional.
7. Exibir vagas ordenadas por score.
8. Preparar a candidatura para revisão manual.
9. Futuramente, usar uma extensão de navegador para preencher campos em páginas reais.

Nesta fase do MVP, o backend já está sendo preparado para:

- subir uma API com FastAPI;
- conectar no PostgreSQL via SQLAlchemy;
- coletar vagas da Remotive;
- listar vagas salvas;
- pesquisar vagas por palavra-chave;
- calcular aderência ao perfil salvo em `profile/profile.json`.

---

## 2. Escopo do MVP

### O que entra no MVP

- API local com FastAPI.
- Banco PostgreSQL via Docker Compose.
- Perfil profissional em JSON.
- Banco de respostas padrão em JSON.
- Coleta de vagas da Remotive.
- Normalização das vagas coletadas.
- Persistência em banco.
- Upsert para evitar duplicidade por `source + external_id`.
- Listagem e busca de vagas.
- Score de aderência com base no perfil profissional.
- Recomendação automática: `CANDIDATAR`, `AVALIAR` ou `DESCARTAR`.

### O que fica para próximas fases

- Frontend em React.
- Extensão Chrome/Edge para preenchimento assistido.
- Conectores adicionais: Remote OK, We Work Remotely, Remotar, Trampos, 99Freelas etc.
- Uso de IA para perguntas abertas.
- Seleção automática de currículo por tipo de vaga.
- Histórico completo de candidaturas.
- Autenticação local.
- Alembic para migrations.
- Dashboard de métricas.

### O que não deve ser feito neste MVP

- Enviar candidaturas automaticamente.
- Clicar no botão final de envio.
- Tentar contornar CAPTCHA.
- Armazenar senhas de plataformas de vagas.
- Fazer scraping agressivo.
- Executar coletas em massa sem controle.
- Inventar experiências, certificações ou informações profissionais.

---

## 3. Arquitetura atual

```text
job-assistant/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── health.py
│   │   │       └── jobs.py
│   │   ├── connectors/
│   │   │   ├── base.py
│   │   │   ├── remotive.py
│   │   │   ├── remote_ok.py
│   │   │   └── we_work_remotely.py
│   │   ├── core/
│   │   │   ├── database.py
│   │   │   └── settings.py
│   │   ├── models/
│   │   │   └── job.py
│   │   ├── repositories/
│   │   │   └── job_repository.py
│   │   ├── schemas/
│   │   │   ├── job.py
│   │   │   └── match.py
│   │   ├── scoring/
│   │   │   └── job_matcher.py
│   │   ├── services/
│   │   │   ├── job_collection.py
│   │   │   └── profile_service.py
│   │   └── main.py
│   ├── .env
│   └── requirements.txt
├── documents/
├── extension/
│   └── test-form.html
├── frontend/
├── profile/
│   ├── profile.json
│   └── answers.json
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 4. Tecnologias utilizadas

### Backend

- Python 3.12
- FastAPI
- Uvicorn
- SQLAlchemy
- Psycopg
- Pydantic
- Pydantic Settings
- HTTPX
- BeautifulSoup

### Banco de dados

- PostgreSQL 16
- Docker Compose

### Futuro frontend

- React
- TypeScript
- Vite

### Futura extensão

- Chrome Extension Manifest V3
- JavaScript ou TypeScript
- Content Scripts
- API local do backend

---

## 5. Requisitos locais

Antes de executar o projeto, é necessário ter instalado:

- Python 3.12+
- Docker Desktop
- Docker Compose
- Git
- VS Code ou IDE equivalente

No Windows, é importante que o Docker Desktop esteja rodando com suporte a WSL 2.

---

## 6. Configuração do ambiente

### 6.1. Clonar ou acessar o projeto

```powershell
cd "C:\Projects\Project Job-Assistant\job-assistant"
```

### 6.2. Criar e ativar o ambiente virtual

Entre na pasta do backend:

```powershell
cd backend
```

Crie o ambiente virtual, caso ainda não exista:

```powershell
python -m venv .venv
```

Ative:

```powershell
.\.venv\Scripts\Activate.ps1
```

O terminal deve exibir algo parecido com:

```text
(.venv) PS C:\Projects\Project Job-Assistant\job-assistant\backend>
```

### 6.3. Instalar dependências

```powershell
python -m pip install fastapi uvicorn sqlalchemy "psycopg[binary]" pydantic-settings httpx beautifulsoup4
```

Gerar ou atualizar `requirements.txt`:

```powershell
pip freeze > requirements.txt
```

---

## 7. Configuração do PostgreSQL

O banco roda via Docker Compose.

### 7.1. Arquivo `docker-compose.yml`

O projeto usa a porta `5433` no Windows para evitar conflito com uma possível instalação local do PostgreSQL na porta `5432`.

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: job-assistant-postgres
    restart: unless-stopped

    environment:
      POSTGRES_DB: jobassistant
      POSTGRES_USER: jobassistant
      POSTGRES_PASSWORD: jobassistant

    ports:
      - "127.0.0.1:5433:5432"

    volumes:
      - job_assistant_postgres_data:/var/lib/postgresql/data

    healthcheck:
      test:
        - CMD-SHELL
        - pg_isready -U jobassistant -d jobassistant
      interval: 5s
      timeout: 5s
      retries: 10

volumes:
  job_assistant_postgres_data:
```

### 7.2. Subir o PostgreSQL

Na raiz do projeto:

```powershell
cd "C:\Projects\Project Job-Assistant\job-assistant"
```

Execute:

```powershell
docker compose up -d
```

Verifique:

```powershell
docker compose ps
```

Resultado esperado:

```text
job-assistant-postgres   Up (healthy)   127.0.0.1:5433->5432/tcp
```

### 7.3. Testar conexão do banco

```powershell
docker compose exec postgres psql -U jobassistant -d jobassistant -c "SELECT current_user, current_database();"
```

Resultado esperado:

```text
 current_user | current_database
--------------+------------------
 jobassistant | jobassistant
```

### 7.4. Recriar banco em caso de erro de senha ou volume antigo

Como estamos no MVP, se o banco ainda não tiver dados importantes, pode recriar tudo:

```powershell
docker compose down -v --remove-orphans
docker compose up -d --force-recreate
```

Atenção: `down -v` remove o volume e apaga os dados do banco.

---

## 8. Configuração do backend

### 8.1. Arquivo `backend/.env`

```env
APP_NAME=Job Application Assistant API
APP_VERSION=0.1.0
DATABASE_URL=postgresql+psycopg://jobassistant:jobassistant@127.0.0.1:5433/jobassistant
```

### 8.2. Arquivo `backend/app/core/settings.py`

Responsável por carregar configurações do `.env` e localizar os arquivos do perfil.

```python
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "Job Application Assistant API"
    app_version: str = "0.1.0"

    database_url: str = (
        "postgresql+psycopg://"
        "jobassistant:jobassistant@127.0.0.1:5433/jobassistant"
    )

    profile_path: Path = PROJECT_ROOT / "profile" / "profile.json"
    answers_path: Path = PROJECT_ROOT / "profile" / "answers.json"

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / "backend" / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
```

### 8.3. Verificar URL de conexão lida pela aplicação

Dentro de `backend`:

```powershell
python -c "from app.core.settings import settings; print(settings.database_url)"
```

Resultado esperado:

```text
postgresql+psycopg://jobassistant:jobassistant@127.0.0.1:5433/jobassistant
```

---

## 9. Executando a API

Dentro de `backend`:

```powershell
cd "C:\Projects\Project Job-Assistant\job-assistant\backend"
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Resultado esperado:

```text
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

Acesse:

```text
http://127.0.0.1:8000
```

Resposta esperada:

```json
{
  "application": "Job Application Assistant API",
  "version": "0.1.0",
  "status": "running",
  "docs": "/docs"
}
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 10. Endpoints disponíveis

### 10.1. Health check

```http
GET /api/health
```

Verifica se a API consegue acessar o PostgreSQL.

Resposta esperada:

```json
{
  "status": "ok",
  "database": "connected"
}
```

---

### 10.2. Coletar vagas da Remotive

```http
POST /api/jobs/collect/remotive?limit=20
```

Busca vagas da Remotive e salva no banco.

Resposta esperada na primeira execução:

```json
{
  "source": "REMOTIVE",
  "received": 20,
  "inserted": 20,
  "updated": 0
}
```

Resposta esperada em uma segunda execução com as mesmas vagas:

```json
{
  "source": "REMOTIVE",
  "received": 20,
  "inserted": 0,
  "updated": 20
}
```

---

### 10.3. Listar vagas

```http
GET /api/jobs
```

Filtros suportados:

```text
source
search
status
skip
limit
```

Exemplos:

```text
http://127.0.0.1:8000/api/jobs?limit=20
http://127.0.0.1:8000/api/jobs?search=java
http://127.0.0.1:8000/api/jobs?search=spring
http://127.0.0.1:8000/api/jobs?search=aws
```

---

### 10.4. Detalhar vaga

```http
GET /api/jobs/{job_id}
```

Exemplo:

```text
http://127.0.0.1:8000/api/jobs/1
```

---

### 10.5. Listar vagas com score

```http
GET /api/jobs/matches
```

Filtros suportados:

```text
source
search
status
min_score
skip
limit
```

Exemplos:

```text
http://127.0.0.1:8000/api/jobs/matches?limit=20
http://127.0.0.1:8000/api/jobs/matches?min_score=70
http://127.0.0.1:8000/api/jobs/matches?search=java&limit=20
http://127.0.0.1:8000/api/jobs/matches?search=aws&limit=20
```

---

### 10.6. Calcular score de uma vaga específica

```http
GET /api/jobs/{job_id}/match
```

Exemplo:

```text
http://127.0.0.1:8000/api/jobs/1/match
```

---

## 11. Perfil profissional

O perfil fica em:

```text
profile/profile.json
```

Ele contém informações usadas pelo motor de aderência:

- dados pessoais básicos;
- cargos desejados;
- modalidades aceitas;
- tipos de contrato;
- regiões aceitas;
- skills principais;
- skills secundárias;
- skills de arquitetura;
- senioridade;
- remuneração mínima e desejada;
- regras de exclusão.

Exemplo de estrutura:

```json
{
  "personal": {
    "full_name": "Anderson de Souza Alves",
    "email": "",
    "phone": "",
    "country": "Brazil",
    "city": "Brasilia",
    "linkedin": "",
    "github": "",
    "english_level": "Fluent",
    "availability": "Immediate"
  },
  "target": {
    "roles": [
      "Senior Software Engineer",
      "Senior Java Developer",
      "Backend Engineer",
      "Java Tech Lead",
      "Software Architect",
      "Solutions Architect"
    ],
    "work_modes": ["Remote"],
    "employment_types": ["Contractor", "Full-time", "PJ", "CLT"],
    "accepted_regions": ["Worldwide", "Latin America", "Brazil", "Americas"]
  },
  "skills": {
    "primary": ["Java", "Spring Boot", "Microservices", "AWS", "REST API", "PostgreSQL"],
    "secondary": ["Kafka", "Docker", "Kubernetes", "Redis", "MongoDB", "Azure", "GCP", "Terraform", "GitHub Actions"],
    "architecture": ["DDD", "Hexagonal Architecture", "Clean Architecture", "CQRS", "SAGA", "Event-driven architecture"]
  },
  "experience": {
    "total_years": 20,
    "java_since": 2005,
    "seniority": ["Senior", "Lead", "Architect", "Staff"]
  },
  "compensation": {
    "minimum_usd_hourly": 30,
    "target_usd_hourly": 36,
    "minimum_brl_monthly": 22000,
    "salary_unknown_accepted": true
  },
  "exclusions": {
    "roles": ["Junior", "Intern", "Trainee"],
    "locations": ["US only without sponsorship", "On-site outside Brazil"]
  }
}
```

---

## 12. Banco de respostas

O banco de respostas fica em:

```text
profile/answers.json
```

Ele será usado futuramente para preencher perguntas abertas em formulários de candidatura.

Exemplo:

```json
{
  "english_level": {
    "question_patterns": [
      "what is your english level",
      "english proficiency",
      "nível de inglês"
    ],
    "answer": "Fluent. I have experience communicating and collaborating with international and distributed teams."
  },
  "availability": {
    "question_patterns": [
      "when can you start",
      "availability",
      "quando pode começar"
    ],
    "answer": "I am available to start immediately."
  }
}
```

---

## 13. Modelo de dados atual

### Tabela `jobs`

| Campo | Descrição |
|---|---|
| `id` | ID interno da vaga |
| `source` | Fonte da vaga, exemplo: `REMOTIVE` |
| `external_id` | ID original da vaga na fonte |
| `title` | Título da vaga |
| `company` | Empresa |
| `category` | Categoria |
| `description` | Descrição limpa em texto |
| `location` | Localização ou restrição geográfica |
| `employment_type` | Tipo de contrato |
| `salary_text` | Texto salarial, quando disponível |
| `application_url` | URL para candidatura |
| `source_url` | URL original da vaga |
| `published_at` | Data de publicação |
| `content_hash` | Hash de título + empresa + localização |
| `status` | Status interno da vaga |
| `collected_at` | Data de coleta |
| `updated_at` | Última atualização |

### Identificação de duplicidade

A regra atual evita duplicidade por:

```text
source + external_id
```

Exemplo:

```text
REMOTIVE + 1234567
```

O campo `content_hash` será usado futuramente para encontrar possíveis duplicidades entre fontes diferentes.

---

## 14. Motor de aderência

O motor de aderência fica em:

```text
backend/app/scoring/job_matcher.py
```

Ele compara cada vaga com `profile/profile.json` e calcula uma pontuação de 0 a 100.

### Critérios atuais

| Critério | Peso máximo |
|---|---:|
| Cargo/título | 20 |
| Skills principais e secundárias | 40 |
| Localização/modalidade | 20 |
| Senioridade | 10 |
| Tipo de contrato | 10 |
| **Total** | **100** |

### Recomendações

| Score | Recomendação |
|---:|---|
| 80 a 100 | `CANDIDATAR` |
| 60 a 79 | `AVALIAR` |
| 0 a 59 | `DESCARTAR` |

### Regras de descarte objetivo

Uma vaga pode ser marcada como `DESCARTAR` mesmo com algum score positivo quando detectar:

- vaga júnior;
- estágio/internship;
- trainee;
- restrição aparente aos EUA;
- cargo presente na lista de exclusão do perfil.

---

## 15. Fluxo de coleta da Remotive

```text
POST /api/jobs/collect/remotive
        ↓
JobCollectionService
        ↓
RemotiveConnector
        ↓
API Remotive
        ↓
NormalizedJob
        ↓
JobRepository.upsert()
        ↓
PostgreSQL jobs
```

---

## 16. Fluxo de score

```text
GET /api/jobs/matches
        ↓
JobRepository.list_jobs()
        ↓
load_profile()
        ↓
JobMatcher(profile)
        ↓
matcher.match(job)
        ↓
JobMatchResponse
```

---

## 17. Comandos úteis

### Subir banco

```powershell
docker compose up -d
```

### Parar banco

```powershell
docker compose down
```

### Apagar banco e volume

```powershell
docker compose down -v
```

### Ver containers

```powershell
docker compose ps
```

### Logs do PostgreSQL

```powershell
docker compose logs postgres --tail 50
```

### Acessar o PostgreSQL

```powershell
docker compose exec postgres psql -U jobassistant -d jobassistant
```

### Contar vagas

```powershell
docker compose exec postgres psql -U jobassistant -d jobassistant -c "SELECT COUNT(*) FROM jobs;"
```

### Listar últimas vagas

```powershell
docker compose exec postgres psql -U jobassistant -d jobassistant -c "SELECT id, source, title, company FROM jobs ORDER BY id DESC LIMIT 10;"
```

### Rodar backend

```powershell
cd "C:\Projects\Project Job-Assistant\job-assistant\backend"
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

### Testar imports principais

```powershell
python -c "from app.models.job import Job; print('Modelo OK:', Job.__tablename__)"
python -c "from app.schemas.job import NormalizedJob; print('Schema OK')"
python -c "from app.repositories.job_repository import JobRepository; print('Repositório OK')"
python -c "from app.services.job_collection import JobCollectionService; print('Serviço OK')"
python -c "from app.scoring.job_matcher import JobMatcher; print('Job matcher OK')"
```

### Testar conector da Remotive sem banco

```powershell
python -c "import asyncio; from app.connectors.remotive import RemotiveConnector; jobs=asyncio.run(RemotiveConnector().fetch_jobs(5)); print('Quantidade:', len(jobs)); print('Primeira vaga:', jobs[0].title if jobs else 'Nenhuma vaga')"
```

---

## 18. Problemas comuns e soluções

### Docker não conecta no Linux Engine

Erro comum:

```text
open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified
```

Solução:

1. Abrir Docker Desktop.
2. Aguardar o engine iniciar.
3. Testar:

```powershell
docker version
docker run --rm hello-world
```

---

### PostgreSQL rejeita senha

Erro comum:

```text
FATAL: password authentication failed for user "jobassistant"
```

Soluções:

1. Confirmar `DATABASE_URL`.
2. Confirmar porta `5433`.
3. Recriar o volume se estiver em MVP:

```powershell
docker compose down -v --remove-orphans
docker compose up -d --force-recreate
```

---

### Porta 5432 em conflito

O projeto usa:

```text
127.0.0.1:5433 -> container:5432
```

Se houver PostgreSQL local no Windows usando `5432`, não precisa desinstalar. Use `5433` para este projeto.

---

### `ModuleNotFoundError: No module named app`

Causa comum: iniciar o Uvicorn na pasta errada.

Execute sempre dentro de:

```text
job-assistant/backend
```

Comando correto:

```powershell
python -m uvicorn app.main:app --reload
```

---

### `ImportError: cannot import name 'Job'`

Verifique:

```text
backend/app/models/job.py
```

O arquivo precisa conter:

```python
class Job(Base):
    __tablename__ = "jobs"
```

Também confirme:

```text
backend/app/models/__init__.py
```

Conteúdo esperado:

```python
from app.models.job import Job

__all__ = ["Job"]
```

---

### `ImportError: cannot import name 'NormalizedJob'`

Verifique:

```text
backend/app/schemas/job.py
```

O arquivo precisa conter:

```python
class NormalizedJob(BaseModel):
```

---

### Limpar cache Python

```powershell
Get-ChildItem -Path .\app -Recurse -Directory -Filter "__pycache__" |
    Remove-Item -Recurse -Force
```

---

## 19. Cuidados com segurança e ética

Este projeto deve seguir uma abordagem controlada:

- Não clicar automaticamente no envio final da candidatura.
- Não tentar contornar CAPTCHA.
- Não simular comportamento humano para burlar bloqueios.
- Não fazer scraping agressivo.
- Respeitar limites e termos de cada plataforma.
- Não armazenar senha de portais de vaga.
- Não versionar dados pessoais, currículos ou chaves de API.
- Não usar IA para inventar experiências.
- Manter revisão humana antes de qualquer candidatura.

---

## 20. Arquivos que não devem ir para o Git

O `.gitignore` deve conter pelo menos:

```gitignore
.env
backend/.env
.venv/
backend/.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.DS_Store
.vscode/settings.json
profile/profile.json
profile/answers.json
documents/*.pdf
documents/*.docx
playwright/.auth/
auth.json
storage-state.json
```

Se quiser versionar exemplos, crie arquivos como:

```text
profile/profile.example.json
profile/answers.example.json
```

---

## 21. Roadmap

### Fase 1 — Fundação

- [x] Criar estrutura do projeto.
- [x] Configurar ambiente Python.
- [x] Configurar Docker Compose.
- [x] Subir PostgreSQL.
- [x] Configurar FastAPI.
- [x] Criar modelo `Job`.
- [x] Criar endpoint `/api/health`.

### Fase 2 — Coleta inicial

- [x] Criar schema `NormalizedJob`.
- [x] Criar interface `JobConnector`.
- [x] Criar conector Remotive.
- [x] Criar `JobRepository`.
- [x] Criar `JobCollectionService`.
- [x] Criar endpoint de coleta.
- [x] Criar endpoints de listagem e detalhe.

### Fase 3 — Aderência ao perfil

- [x] Criar `profile_service.py`.
- [x] Criar `JobMatcher`.
- [x] Criar schema `JobMatchResponse`.
- [x] Criar endpoint `/api/jobs/matches`.
- [x] Criar endpoint `/api/jobs/{id}/match`.

### Fase 4 — Frontend

- [ ] Criar projeto React com Vite.
- [ ] Criar tela de listagem de vagas.
- [ ] Mostrar score e recomendação.
- [ ] Criar filtros por score, fonte e termo.
- [ ] Criar página de detalhe.
- [ ] Botão “Abrir candidatura”.
- [ ] Botão “Descartar”.
- [ ] Botão “Marcar para revisar”.

### Fase 5 — Extensão

- [ ] Criar Manifest V3.
- [ ] Criar popup da extensão.
- [ ] Ler campos da página.
- [ ] Mapear labels e placeholders.
- [ ] Buscar perfil no backend local.
- [ ] Preencher campos conhecidos.
- [ ] Exigir revisão para campos ambíguos.
- [ ] Nunca clicar em Submit.

### Fase 6 — IA assistida

- [ ] Criar banco de fatos profissionais.
- [ ] Gerar respostas para perguntas abertas.
- [ ] Validar respostas contra fatos reais.
- [ ] Exigir revisão humana.
- [ ] Salvar respostas aprovadas.

### Fase 7 — Novos conectores

- [ ] Remote OK.
- [ ] We Work Remotely.
- [ ] Jobspresso.
- [ ] Working Nomads.
- [ ] Skip The Drive.
- [ ] Remotar.
- [ ] Trampos.co.
- [ ] 99Freelas.
- [ ] Indeed Brasil.
- [ ] Upwork.
- [ ] Freelancer.com.

---

## 22. Próximo passo recomendado

O próximo passo técnico é criar o **frontend simples em React**, consumindo os endpoints já existentes:

```text
GET /api/jobs/matches?limit=50
GET /api/jobs/{id}/match
POST /api/jobs/collect/remotive
```

A primeira tela deve mostrar:

- título da vaga;
- empresa;
- fonte;
- localização;
- score;
- recomendação;
- skills encontradas;
- skills ausentes;
- botão para abrir a candidatura;
- botão para descartar;
- botão para revisar depois.

---

## 23. Status atual do MVP

O projeto está na fase de backend local, com PostgreSQL e FastAPI.

O objetivo imediato é garantir que os seguintes endpoints funcionem corretamente:

```text
GET  /api/health
POST /api/jobs/collect/remotive
GET  /api/jobs
GET  /api/jobs/matches
GET  /api/jobs/{id}/match
```

Quando esses endpoints estiverem estáveis, o desenvolvimento pode avançar para o frontend e, depois, para a extensão de preenchimento assistido.
