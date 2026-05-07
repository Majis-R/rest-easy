# Sprint 1
- Planned 10 hours of work, completed in 3. Did a lot of the work during previous week
- core
	- registry
        - Explicit Module loading via `main.py`
    - module protocol definition (forces loose coupling, modules only "attach" to the app)
- Hello world module (proof of concept for routing and dependency injection)
*Status: Completed*
# Sprint 2
- Planned 10 hours of work
- Plug and play authentication modules for future modules to use
	- Password module (Just password auth with a set password, no account based access controll, JWT tokens)
	- Account module (Full account based access controll)
- Setup asynchronous PostgreSQL engine & Docker orchestration
- CLI tooling for secure admin account bootstrapping
- Local HTTPS/TLS using mkcert in Docker
*Status: Completed*
# Sprint 3
- Planned 10 hours of work
- Implement Security Middleware (CORS, HSTS)
- Implement Rate Limiting to prevent brute-force attacks
- Develop the final demonstration module (e.g., Chat API) securely using the Account auth dependency.
*Status: Completed*