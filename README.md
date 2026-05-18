Student ID:H293110
# Rest Easy
Rest Easy is built as a modular monolithic framework template that is designed to be easily modified into a desired secure API. 
This repository contains the rest easy sourcecode that has been modified to function as the backend of a simple chat application. The front end for the chat app is under a separate repository https://github.com/Majis-R/Bubly-front-end. The backend is deployed at https://bubly.duckdns.org/ and the frontend is deployed to https://majis-r.github.io/Bubly-front-end/ The frontend and the backend are separated in order to more effectively demonstrate features such as CORS handling and API requests via HTTPS. The presentaion slides can also be found in this repository. 

The API endpoints and schemas of the running configuration are documented and can also be tested right at the backend service (see `/docs` and `/redoc`). This README serves as the focuses on architecture, security decisions, learning outcomes, and design alignment.

## Quick start (local)
Local execution is not the primary deployment path, but it is possible for development, though it has not been tested in a while:
1. Create and populate a `.env` file (see Environment below).
2. Start the database: `docker compose up -d db`
3. Run the API: `python -m uvicorn app.main:app --reload`
4. Open the test UI: https://127.0.0.1:8000/test-ui
Local certificates can be set up with mkcert if desired

## Environment
The app uses strongly typed environment variables in [app/core/secrets.py](app/core/secrets.py). These can be included as an .env file for local development or be injected from Jenkins secret as a part of the deployment pipeline 

Required variables:
- `DATABASE_URL`
- `SECRET_KEY`
- `COMMON_PASSWORD`
- `ENVIRONMENT`
- `CORS_ORIGINS` (JSON list or a single origin)

## Architecture (design vs implementation)
The architectural goals and planned features are captured in [DesignDoc.md](DesignDoc.md). The implementation follows those plans with some explicit gaps (listed below).

**Design decisions that are implemented**
- Modular monolith with a registry in [app/core/registry.py](app/core/registry.py) and protocol in [app/core/module_protocol.py](app/core/module_protocol.py).
- Async SQLAlchemy engine and per-request sessions in [app/core/database.py](app/core/database.py).
- Modules registered explicitly in [app/main.py](app/main.py).
- Demo modules: account auth and chat are enabled; the older password-only auth module is present but not registered.

**Design items not yet implemented**
- Account lockout after repeated failed logins.
- Suspicious activity logging and incident response pipeline.
- IP-based restrictions beyond rate limiting.
- Error response standardization and suppression of sensitive details.
- Explicit output encoding for XSS defense.

### Example data flow
For a protected chat route like `GET /chat/messages`, the request is routed to the chat module router, which enforces `auth` from the account module as a dependency. The JWT is validated, the user is loaded from the database, and the handler calls the chat service, which uses an async SQLAlchemy session to query messages. The service returns data to the router, which serializes it with Pydantic response schemas and returns JSON to the client.

### Modifying the project. 
As the project was built to be a framework it was designed to be easy to modify. The modification to a different type of API would happen by writing a module with a similar format to the included example of the chat module. The endpoints can be made protected by authentication just by making the require one of the two different auth modules chosen depending on the type of authentication required. After this the module would have to registered in [main.py](main.py)

### Module design
The modules can have multiple different files. Each module can contain some or all of the following files the funtionality of each of the file types is explained here:
- **module.py** Called by [registry.py](registry.py) in order to register each module. The module definition is given in [module_protocol.py](module_protocol.py)
- **models.py** Defines the persistence layer for the module, usually SQLAlchemy models and table mappings for stored data.
- **router.py** Declares the HTTP routes and request handlers, wiring dependencies and calling the service layer.
- **schemas.py** Defines Pydantic request/response models used for validation and serialization at the API boundary.
- **services.py** Holds the module business logic and database operations that are called by the routers and other modules as well.
- **dependencies.py** Centralizes FastAPI dependency functions (auth, permissions, shared context) used by the routers. Can be imported by other modules in order to protect routes with authentication.

Shared components are defined in the core folder

## Security decisions
The security plan in [DesignDoc.md](DesignDoc.md) is reflected in the codebase. Highlights below include small code excerpts to show where decisions live.

### Forcing HTTPS
The API was designed to be only intercatable through an https connection to ensure end to end TLS encryption. HTTPS certificates ate implemented with Let's Encrypt. Thge initalisation script for the let's encrypt was more complex for containarized setup. This site: https://dev.to/marrouchi/the-challenge-about-ssl-in-docker-containers-no-one-talks-about-32gh was used as a guide for settig up a startup script [init-letsencrypt.sh](init-letsencrypt.sh) that is ran as a part of the jenkins pipeline defined in the [Jenkinsfile](Jenkinsfile)

### Password hashing (Argon2id via Passlib)
Stored passwords are hashed using Argon2 through Passlib:

```python
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

See [app/modules/account_auth/services.py](app/modules/account_auth/services.py).

### Stateless auth with expiring JWTs
The account login flow issues a JWT with an expiration ($1$ hour):

```python
payload = {
    "sub": username,
    "role": role,
    "iat": int(time.time()),
    "exp": int(time.time()) + 3600
}
```

See [app/modules/account_auth/router.py](app/modules/account_auth/router.py).

### Role-based access control (RBAC)
Authenticated routes can be set up to use the the password auth module or the account auth module dependency to implement authentication of endpoints `auth_admin` dependency to enforce roles:

```python
if current_user.role != "admin":
    raise HTTPException(status_code=403, detail="You do not have enough privileges")
```

See [app/modules/account_auth/dependencies.py](app/modules/account_auth/dependencies.py).

### Avoid raw SQL entirely
The program uses only parametarized querys using SQLAlchemy’s ORM and select() constructs. These patterns ensure SQLAlchemy binds parameters safely rather than interpolating strings.

### Use schemas 
Pydantic is used to define schemas for input data. This means that FastAPI rejects requests that do not match the declared types and constraints. That means malformed or unexpected payloads are blocked at the boundary.

### Rate limiting
Default rate limits are set globally and tightened on login/register routes:

```python
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
```

See [app/core/rate_limit.py](app/core/rate_limit.py) and [app/modules/account_auth/router.py](app/modules/account_auth/router.py).

### Security headers and HTTPS
The app adds security headers at the application layer:

```python
response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
response.headers["X-Content-Type-Options"] = "nosniff"
response.headers["X-Frame-Options"] = "DENY"
response.headers["X-XSS-Protection"] = "1; mode=block"
```

See [app/main.py](app/main.py).

At the edge, Nginx terminates TLS and redirects HTTP to HTTPS in [nginx/default.conf](nginx/default.conf).

### Secrets and admin provisioning
Secrets are loaded from environment variables in [app/core/secrets.py](app/core/secrets.py). These are intended to be provided as Jenkins secrets. Admin accounts are created out-of-band via the local CLI [create_admin.py](create_admin.py) to keep privileged provisioning entirely off public endpoints.

### Automatic SBOM generation
SBOMs are generated automatically as part of the deployment pipeline with CycloneDX based on the requirements file used to puild the application [requirements.txt](requirements.txt). The generated SBOM file [sbom.json](sbom.json) has been included in this repository in order to show the file as proof of the sbom generation working. 

## Demo deployment (CSC Pouta)
The app is configured as a demo service on CSC Pouta. The primary deployment method is the Jenkins pipeline in [Jenkinsfile](Jenkinsfile), which provisions certificates and deploys the stack. The deployment stack includes:
- Docker Compose for API + Postgres + Nginx + Certbot in [docker-compose.yml](docker-compose.yml).
- TLS termination and HTTP->HTTPS redirect in [nginx/default.conf](nginx/default.conf).
- Let's Encrypt bootstrap in [init-letsencrypt.sh](init-letsencrypt.sh).

The Nginx configuration currently targets the demo domain `bubly.duckdns.org`, and the API is proxied to the internal `api:8000` service.

The API is available directly at https://bubly.duckdns.org/ and its documentation is available at https://bubly.duckdns.org/docs.

## Demo integration
The API is currently configured to act as the backend for the Bubly front-end demo application:
- Front-end repository: https://github.com/Majis-R/Bubly-front-end
- Live site: https://majis-r.github.io/Bubly-front-end/

## Testing
Testing was limited due to time restraints
- TLS encryption was verified with Wireshark.
- CORS behavior was checked with `curl` against allowed and disallowed origins.
- Because the database runs in a separate container, connectivity was tested to confirm it is not directly reachable outside the Docker network without explicit port exposure.
- General testing of the API endpoitns was done during the development cycle.

## Known limitations and next steps
These are aligned with the gaps listed in [DesignDoc.md](DesignDoc.md) and the TODOs in the code:
- No account lockout or suspicious activity logging yet.
- No centralized error response shape.
- Password complexity requirements are intentionally minimal for the demo.
- Search uses `ilike` with a wildcard; ORM parameterization mitigates SQL injection, but input hardening could be stricter.
- The API is not IP-restricted for demo purposes; if desired, add IP allow/deny rules in [nginx/default.conf](nginx/default.conf) or enforce access control via security groups or host firewall rules.
- Vulnerability monitoring could be made more automatic by making the pipeline produce an artefact from pip-audit. Currently this needs to be done manually
- While some of the OWASP Cheat sheets were red through and considered for implemetning the program I could have been more thorrow with documenteing my reasonings. 
- No automatic deployment was setup for when a push to the main branch happens in the remote. This was considered but had to be cut for time.
- As described in the testing subsection testing of the application was rather limited due to time constraints. I wanted to try to try attacking the api but could not make the time to do this.


## Files worth reading
- [DesignDoc.md](DesignDoc.md) for the original plan and rationale.
- [app/main.py](app/main.py) for middleware, headers, CORS, and module registration.
- [app/modules/account_auth](app/modules/account_auth) for auth flow and RBAC.
- [app/modules/chat_module](app/modules/chat_module) for the demo resource and access control.

## AI usage
AI was utilized in the project for:
- Project idea brainstorming
- Planning
- Code production
- Debugging
- Documentation
  
Generally any output of the AI was carefully reviewed in places that were deemed important to security. AI was mostly a useful tool in this case. It did get hung up on many things and required a lot of manual intervention

## Learing outcomes
I laid out multiple learning goals for this project. These included learning to:
- Set up HTTPS certificates with Let's Encrypt
- Deepen my understanding of containers
- Build my first propper API
- Deepen my understanding of jenkins and CI/CD in general
- Learn what CORS is and how it works
- Learn about JWT 
I would say that these learning goals have been met. 
