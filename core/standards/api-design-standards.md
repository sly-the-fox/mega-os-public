# API Design Standards

Standards for designing and reviewing APIs across all products. Apply to REST APIs, CLI interfaces with HTTP backends, and MCP tool definitions.

---

## URL Conventions

- Use lowercase with hyphens: `/user-profiles`, not `/userProfiles` or `/user_profiles`
- Use plural nouns for collections: `/documents`, `/users`
- No verbs in URLs — use HTTP methods for actions: `POST /documents` not `POST /create-document`
- Nest for clear ownership: `/users/{id}/documents`
- Maximum nesting depth: 2 levels (`/a/{id}/b/{id}`)
- Use query parameters for filtering, sorting, and pagination: `/documents?status=active&sort=created_at`

## HTTP Methods

| Method | Purpose | Idempotent | Request Body |
|--------|---------|------------|--------------|
| GET | Retrieve resource(s) | Yes | No |
| POST | Create resource | No | Yes |
| PUT | Full replace | Yes | Yes |
| PATCH | Partial update | No | Yes |
| DELETE | Remove resource | Yes | No |

- Return `201 Created` for POST with `Location` header
- Return `204 No Content` for DELETE (or `200` with the deleted resource)
- Return `200` for successful GET, PUT, PATCH

## Response Envelope

Use a consistent response structure:

```json
{
  "data": { ... },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-03-11T14:30:00Z"
  }
}
```

For collections:

```json
{
  "data": [ ... ],
  "meta": {
    "total": 142,
    "cursor": "eyJpZCI6MTQyfQ==",
    "has_more": true
  }
}
```

## Error Format

```json
{
  "error": {
    "code": "validation_error",
    "message": "Human-readable description",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  }
}
```

- `code`: machine-readable error type (snake_case)
- `message`: human-readable explanation
- `details`: optional array of field-level errors

Standard error codes: `validation_error`, `not_found`, `unauthorized`, `forbidden`, `conflict`, `rate_limited`, `internal_error`

## HTTP Status Codes

| Code | When |
|------|------|
| 200 | Success |
| 201 | Created |
| 204 | No content (successful DELETE) |
| 400 | Validation error, malformed request |
| 401 | Missing or invalid authentication |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate, state conflict) |
| 422 | Semantically invalid (valid JSON, bad values) |
| 429 | Rate limited |
| 500 | Internal server error |

## Versioning

- Preferred: URL prefix versioning (`/v1/documents`)
- Version only when making breaking changes
- Breaking changes: removing fields, renaming fields, changing field types, removing endpoints
- Non-breaking: adding optional fields, adding new endpoints

## Pagination

- Preferred: cursor-based pagination (`?cursor=abc&limit=20`)
- Supported: offset-based (`?offset=0&limit=20`) for simple use cases
- Default limit: 20, maximum: 100
- Always return `has_more` boolean and `cursor` (or `next_offset`) in meta

## Authentication

- Use `Authorization: Bearer <token>` for user authentication
- Use `X-API-Key: <key>` for service-to-service or API key auth
- Never pass credentials in URL query parameters
- Return `401` for missing/invalid auth, `403` for insufficient permissions

## Rate Limiting

Include these headers in all responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1710000000
```

- `Reset` is a Unix timestamp
- Return `429 Too Many Requests` when limit exceeded
- Include `Retry-After` header with seconds to wait

## General Guidelines

- Use `snake_case` for JSON field names
- Use ISO 8601 for dates and timestamps: `2026-03-11T14:30:00Z`
- Use UUIDs or prefixed IDs (`doc_abc123`) — not sequential integers
- Accept and return UTC timestamps
- Support `Accept: application/json` — return `406` if unsupported format requested
- Include `Content-Type: application/json` in all JSON responses
