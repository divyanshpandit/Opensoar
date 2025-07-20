<img width="1352" height="650" alt="image" src="https://github.com/user-attachments/assets/1ea37a1a-14c2-4131-a1f2-b9ba1cae8bf8" />
**Opensoar** is a lightweight, open-source Security Orchestration, Automation, and Response (SOAR) platform built on Flask. It helps security teams automate incident detection, response, and reporting workflows, maximizing efficiency and minimizing mean time to respond.

## Features

- 🗂️ **Incident Management:** Track, assign, and update security incidents.
- 🔑 **JWT-based Authentication:** Secure API endpoints with JSON Web Token authentication.
- 👤 **User Management:** Register, manage, and assign roles to users.
- 🔌 **API-first Design:** All major functionality exposed via RESTful APIs.
- 🛡️ **Configurable Security:** Leverages best practices for secret management and debug control.
- 🚦 **Role-Based Access Control:** (Planned) Restrict actions based on user roles.
- 📊 **Audit Logging:** (Planned) Record activity for compliance and review.


## Quick Start

### 1. Clone \& Install

```bash
git clone https://github.com/divyanshpandit/Opensoar.git
cd Opensoar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


### 2. Environment Setup

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-very-strong-secret-key
FLASK_ENV=development             # Use 'production' in production
DATABASE_URL=sqlite:///soar.db    # Or your preferred SQLAlchemy DB URI
```

**Important:**

- Never commit your `.env` to version control!
- Use a unique, random `SECRET_KEY` for each environment.
Generate one with:

```python
python -c "import secrets; print(secrets.token_hex(32))"
```


### 3. Database Migration

```bash
flask db init         # Only once, on fresh setup
flask db migrate
flask db upgrade
```


### 4. Run the Application

#### For Development

```bash
export FLASK_ENV=development
flask run
```


#### For Production

```bash
export FLASK_ENV=production
flask db upgrade      # Ensure migrations are applied
gunicorn 'app:create_app()'
```


## API Overview

The API follows RESTful principles.
Example endpoints:

- **User Auth:**
`POST /auth/register` – user registration
`POST /auth/login` – obtain JWT
- **Incidents:**
`GET /api/incidents` – list/query incidents
`POST /api/incidents` – create incident
`PUT /api/incidents/<id>` – update incident
- **Users:**
(See planned RBAC/management endpoints)


### Authentication

All protected endpoints require JWT authentication. Retrieve a token from `/auth/login` and include it with requests:

```
Authorization: Bearer <your_token>
```


## Security

**Best Practices Implemented:**

- 🔒 Secret key loaded from environment variable, never hardcoded
- 🛑 Debug mode is **disabled by default in production**
- 📝 Sensitive files (`.env`, DBs) should be in `.gitignore`
- 🕵️‍♂️ Input validation and password policy (in progress)
- 🔐 Secure JWT, CSRF support (plannned)

**You are responsible for:**

- Setting a secure, random `SECRET_KEY` in your environment
- Running behind HTTPS in production


## Configuration

All settings are controlled with environment variables, loaded via [python-dotenv](https://pypi.org/project/python-dotenv/).


| Variable | Description |
| :-- | :-- |
| `SECRET_KEY` | **Required**. Secret for JWT and Flask session |
| `FLASK_ENV` | Set to `development` or `production` |
| `DATABASE_URL` | SQLAlchemy-compatible database URI |

See [`config.py`](config.py) for more.

## Roadmap

- [x] Basic incident/user APIs
- [ ] Role-based access control
- [ ] Audit trails and logs
- [ ] Advanced response workflows
- [ ] Security improvements (rate limiting, headers, CSRF, etc.)

Bug reports and pull requests are welcome!

## Contributing

1. Fork the repo and create your feature branch.
2. Add your changes with clear commits.
3. Ensure code quality and pass tests.
4. Submit a pull request for review.

## License

MIT © [Divyansh Pandit](https://github.com/divyanshpandit)

## Acknowledgments

Built with Flask, SQLAlchemy, Flask-JWT-Extended, and community collaboration.

**For questions or support, [file an issue](https://github.com/divyanshpandit/Opensoar/issues).**
