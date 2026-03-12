# blog-cms-api

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)
![DRF](https://img.shields.io/badge/DRF-3.14-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)
![pytest](https://img.shields.io/badge/tested%20with-pytest-yellow)

REST API for a Blog CMS — built with Django REST Framework, 
JWT authentication, PostgreSQL and Docker.

## Features

- CRUD for Posts, Categories, Tags and Comments
- JWT authentication (access + refresh tokens)
- Auto-generated slugs for Posts, Categories and Tags
- Comment moderation (approve/reject)
- Pagination on all list endpoints
- Fully containerized with Docker Compose

## Quick Start
```bash
git clone https://github.com/Heresia517/blog-cms-api.git
cd blog-cms-api
cp .env.example .env
docker-compose up --build
```

API available at: `http://localhost:8000/api/`

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/token/ | No | Get JWT tokens |
| POST | /api/token/refresh/ | No | Refresh access token |
| GET | /api/posts/ | No | List published posts |
| POST | /api/posts/ | Yes | Create a post |
| GET | /api/posts/{slug}/ | No | Get post detail |
| PUT | /api/posts/{slug}/ | Yes | Update a post |
| DELETE | /api/posts/{slug}/ | Yes | Delete a post |
| GET | /api/categories/ | No | List categories |
| GET | /api/tags/ | No | List tags |
| GET | /api/posts/{id}/comments/ | No | List comments |
| POST | /api/posts/{id}/comments/ | Yes | Add a comment |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| SECRET_KEY | Django secret key | required |
| DEBUG | Debug mode | False |
| DB_NAME | Database name | blog_cms |
| DB_USER | Database user | postgres |
| DB_PASSWORD | Database password | required |
| DB_HOST | Database host | db |
| DB_PORT | Database port | 5432 |

## Author

**Hezekiah Topan**
- GitHub: [Heresia517](https://github.com/Heresia517)
- LinkedIn: [hezekiah-topan](https://linkedin.com/in/hezekiah-topan)
