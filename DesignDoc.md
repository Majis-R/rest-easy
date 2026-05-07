# Goal:  
Create a RESTful API template/framwork-like-thing that can be easily modified to provide a simple API service (e.g., task manager, notes storage, or user info retrieval) with strong security measures. The API should demonstrate secure coding practices, proper authentication, and mechanisms to prevent abuse.
# Key Features:
1. **Authentication & Authorization**
    - [x] User registration/login
    - [x] Passwords hashed with strong algorithms
    - [x] Token-based authentication
    - [x] Role-based access control
2. **Input Validation & Output Encoding**
    - [x] Validate all incoming data
    - [ ] Prevent injection attacks
    - [ ] Encode responses to prevent XSS
3. **Abuse Protection**
    - [x] Rate limiting per IP/user
    - [ ] Account lockout after repeated failed login attempts
    - [ ] Logging suspicious activity (failed logins, repeated invalid requests)
    -  [ ] IP-based restrictions
4. **Transport Security**
    - [x] Force HTTPS
    - [x] Secure headers (CORS, Content Security Policy, HSTS)
5. **Error Handling**
    - [ ] Avoid exposing sensitive info in errors
    - [ ] Consistent JSON error responses

**Deliverables:**
- Fully functioning, customisable API framework
- Specific demosntration of the framework(Simple chat api)
- Source code with inline comments documenting secure coding decisions
- Report covering:
    - Architecture & endpoints
    - Security measures and mapping to OWASP Top 10/SANS 25
    - Testing (manual + automated)
    - Known limitations and suggestions for improvement
# Considerations
**A. Security Design**
- Threat modeling: who could attack, and what are the attack vectors?
- Authentication: secure password storage, token management, password reset process
- Authorization: endpoint-level access control
- Input sanitization: validate user input to avoid injection attacks
- Transport layer: HTTPS enforcement
- Logging: avoid logging sensitive info, include necessary audit trails
- Rate limiting / throttling to prevent abuse

**B. Implementation Details**
- Endpoint design: what resources and methods (GET/POST/PUT/DELETE)
- Data models: users, sessions, any other resources
- Testing hooks: ways to verify security features manually and automatically
- Deployment considerations: local vs cloud 

**C. Testing & Validation**
- Manual testing: authentication bypass, brute force attempts, injection attacks
- Automated testing: unit tests, API tests, security scanner reports
- Document vulnerabilities discovered and fixes applied

**D. Documentation & Report**
- How the API works and its endpoints
- Architecture diagram
- Secure coding decisions (reference OWASP Top 10 and SANS 25)
- Test results, found vulnerabilities, and remediation
- Known limitations and possible improvements

**E. Additional Enhancements**
- Refresh token implementation
- API key system for third-party clients
- Continuous security testing (automated DevSecOps pipeline)

# Tools
1. Backend **(Python)**
2. Python Web Framework  **(FastAPI)**
3. Database **(PostgreSQL)**
4. Authentication/password management 
	1. Password hashing **(Argon2id)**
	2. Token management **(JWT with Authlib)**
	3. OAUth **(OAuth2 with Authlib)**
5. Input validation **(Pydantic with FastAPI)**
6. Security headers & middleware
	1. HTTPS enforcement **(HTTPSRedirectMiddleware from starlette in FastAPI)**
	2. CORS handling: **(fastapi.middleware.cors)**
7. Rate limiting/Abuse prevention
	1. Rate limiting **(SlowAPI)**
	2. Fast incident logging and response **(Redis)** ==Maybe?==
8. Testing
	1. API requests **(Postman)**
	2. Endpoits **(Firefox)**
	3. Unit and integration testing **(pytest)**
	4. dynamic application security testing **(OWASP ZAP)**
	5. Python static code security analysis **(Bandit)**
	6. dependency vulnerability checking **(pip-audit)**
    7. local certificate authority tool **(mkcert)**
9. Logging & monitoring **(Loguru)**
10. Version control **(Git + GitHub)**
11. Dependency & environment management **(venv + pip)**
12. Documentation/reporting
	1. Markdown files **(Obsidian md)**
	2. UML diagrams **(Plantuml)**
	3. API documanetation **(OpenAPI)**
13. CI/CD & DevSecOps
	1. Some parts of the jenkins pipeline laid out during course

# Architectural Decisions
- Modular Monolith Design: Chosen over true microservices to eliminate internal network latency while still maintaining strict code separation.
- Plug-and-Play Module Registry: Implemented a standardized ModuleProtocol where independent modules attach their own routes to a central registry, keeping the main application logic clean and highly extensible.
- Native Dependency Injection: Leveraged FastAPI's Depends system for cross-module interactions (such as passing database sessions and enforcing authentication) instead of internal HTTP calls.
- Asynchronous Database I/O: Selected asyncpg with SQLAlchemy's async engine to fully utilize FastAPI's asynchronous event loop, allowing the API to handle high concurrent HTTP requests without blocking worker threads.
- Containerized Orchestration: Wrapped the application and its PostgreSQL database entirely in Docker Compose, guaranteeing environment consistency across local development, testing, and future deployments.
- Centralized Configuration Management: Decoupled configuration from the codebase by managing all environment variables, secrets, and database URIs through a strongly-typed Pydantic BaseSettings class.

# Security Decisions
- Secure Password Storage: Adopted Argon2 via Passlib for password hashing, which is currently the industry standard.
- Stateless Authentication: Implemented JSON Web Tokens (JWT) using Authlib with mandatory expiration times (1 hour) to limit the attack window of stolen tokens.
- Role-Based Access Control (RBAC): Created centralized authorization dependencies (e.g., auth and auth_admin) to strictly enforce privileges at the route level.
- SQL Injection Prevention: Exclusively utilized an Object-Relational Mapper (SQLAlchemy) with parameterized queries, completely avoiding raw SQL strings.
- Out-of-Band Admin Provisioning: Kept administrative account creation off the public internet by isolating it to a local CLI script (create_admin.py).
- Secrets Management: Removed all hardcoded secrets and database URIs from source code, relocating them to .env variables parsed by Pydantic.



# Resources
[OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)

[OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

[OWASP OAuth2 Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html)

[OWASP REST Assessment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Assessment_Cheat_Sheet.html)

[OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

[FastAPI HTTPS](https://fastapi.tiangolo.com/deployment/https/)

[FastAPI Security Headers](https://www.compilenrun.com/docs/framework/fastapi/fastapi-security/fastapi-security-headers/)

[HTTP Strict Transport Security (HSTS)](https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security)

[OWASP HTTP Strict Transport Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html)

[FastAPI Advanced Middleware](https://fastapi.tiangolo.com/advanced/middleware/)