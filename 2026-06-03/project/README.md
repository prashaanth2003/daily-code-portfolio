# Go URL Shortener API Service

**Date:** 2026-06-03 | **Language:** Go | **Category:** Systems/Backend

## Endpoints
- `POST /api/shorten` — Create short URL (base62, 7 chars)
- `GET /{code}` — Resolve + 302 redirect
- `GET /api/stats` — System stats
- `GET /api/urls` — List all URLs
- `GET /api/health` — Health check

## Features
Thread-safe (sync.RWMutex), Base62, graceful shutdown, logging middleware.

## Run
```bash
go run main.go     # :8080
go test -v         # 9 tests
```
