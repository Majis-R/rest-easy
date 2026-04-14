# Goal:  
Create a RESTful API template/framwork-like-thing that can be easily modified to provide a simple API service (e.g., task manager, notes storage, or user info retrieval) with strong security measures. The API should demonstrate secure coding practices, proper authentication, and mechanisms to prevent abuse.

# Key Features:
1. **Authentication & Authorization**
    - User registration/login
    - Passwords hashed with strong algorithms
    - Token-based authentication
    - Role-based access control
2. **Input Validation & Output Encoding**
    - Validate all incoming data
    - Prevent injection attacks
    - Encode responses to prevent XSS
3. **Abuse Protection**
    - Rate limiting per IP/user
    - Account lockout after repeated failed login attempts
    - Logging suspicious activity (failed logins, repeated invalid requests)
    -  IP-based restrictions
4. **Transport Security**
    - Force HTTPS
    - Secure headers (CORS, Content Security Policy, HSTS)
5. **Error Handling**
    - Avoid exposing sensitive info in errors
    - Consistent JSON error responses
6. **Optional Advanced Features**
    - Refresh tokens for session management

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
	1. Password hashing **(Argon2id with argon2-cffi)**
	2. Token management **(JWT with Authlib)**
	3. Possible OAUth **(OAuth2 with Authlib)**
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
9. Logging & monitoring **(Loguru)**
10. Version control **(Git + GitHub)**
11. Dependency & environment management **(venv + pip)**
12. Documentation/reporting
	1. Markdown files **(Obsidian md)**
	2. UML diagrams **(Plantuml)**
	3. API documanetation **(OpenAPI)**
13. CI/CD & DevSecOps
	1. Some parts of the jenkins pipeline laid out during course

# Architecture
- Layered Architecture with “Plug-in Style” Resource Modules
- Modules follow a module contract 
- Dependency injection





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