# API Structure

Base path: `/api/`. All endpoints except auth require a valid JWT access token in
the `Authorization: Bearer <token>` header. Ownership scoping (see
permissions-matrix.md) is applied server-side on every list/detail endpoint below —
never trust a role or ownership check on the frontend alone.

## Auth — `apps/users`
| Method | Endpoint                  | Who        | Notes |
|--------|----------------------------|------------|-------|
| POST   | /api/auth/register/       | Public     | role = landlord or tenant at signup |
| POST   | /api/auth/login/          | Public     | returns access + refresh token |
| POST   | /api/auth/refresh/        | Public     | exchanges refresh for new access token |
| POST   | /api/auth/logout/         | Authenticated | blacklists refresh token |
| GET    | /api/auth/me/             | Authenticated | current user profile |
| PATCH  | /api/auth/me/             | Authenticated | update own profile |

## Properties — `apps/properties`
| Method | Endpoint                     | Who      | Notes |
|--------|-------------------------------|----------|-------|
| GET    | /api/properties/              | Landlord | own properties only |
| POST   | /api/properties/              | Landlord | create |
| GET    | /api/properties/{id}/         | Landlord | own only, 404 otherwise |
| PATCH  | /api/properties/{id}/         | Landlord | own only |
| DELETE | /api/properties/{id}/         | Landlord | own only |

## Units — `apps/units`
| Method | Endpoint                                   | Who      | Notes |
|--------|----------------------------------------------|----------|-------|
| GET    | /api/properties/{property_id}/units/         | Landlord | list units under one property |
| POST   | /api/properties/{property_id}/units/         | Landlord | create unit under property |
| GET    | /api/units/{id}/                              | Landlord (own), Tenant (if assigned) | detail |
| PATCH  | /api/units/{id}/                              | Landlord | own only |
| DELETE | /api/units/{id}/                              | Landlord | own only |

## Tenants — `apps/tenants`
| Method | Endpoint                  | Who      | Notes |
|--------|-----------------------------|----------|-------|
| GET    | /api/tenants/                | Landlord | own tenants only (via tenancies) |
| POST   | /api/tenants/invite/         | Landlord | invite/add a tenant (creates User+TenantProfile) |
| GET    | /api/tenants/{id}/           | Landlord (own), Tenant (self) | detail |
| PATCH  | /api/tenants/{id}/           | Landlord (own), Tenant (self, limited fields) | |

## Tenancies — `apps/tenancies`
| Method | Endpoint                     | Who      | Notes |
|--------|-------------------------------|----------|-------|
| GET    | /api/tenancies/                | Landlord (own), Tenant (own) | list |
| POST   | /api/tenancies/                | Landlord | assign tenant to unit |
| GET    | /api/tenancies/{id}/           | Landlord (own), Tenant (own) | detail |
| PATCH  | /api/tenancies/{id}/           | Landlord | update lease dates / rent |
| POST   | /api/tenancies/{id}/end/       | Landlord | end tenancy, frees unit |

## Rent — `apps/rent`
| Method | Endpoint                              | Who      | Notes |
|--------|-----------------------------------------|----------|-------|
| GET    | /api/rent/                               | Landlord (own), Tenant (own) | filter by ?status=&month= |
| GET    | /api/rent/{id}/                          | Landlord (own), Tenant (own) | detail |
| PATCH  | /api/rent/{id}/status/                   | Landlord | mark paid / overdue / cancelled |
| POST   | /api/rent/generate/                      | Landlord (or system/Celery) | generate current month's records |

## Payments — `apps/payments`
| Method | Endpoint                              | Who      | Notes |
|--------|-----------------------------------------|----------|-------|
| POST   | /api/rent/{rent_record_id}/payments/     | Tenant   | upload proof, create payment (own rent record) |
| GET    | /api/payments/                           | Landlord (own), Tenant (own) | history |
| GET    | /api/payments/{id}/                      | Landlord (own), Tenant (own) | detail |
| POST   | /api/payments/{id}/verify/                | Landlord | mark verified/rejected |

## Maintenance — `apps/maintenance`
| Method | Endpoint                              | Who      | Notes |
|--------|-----------------------------------------|----------|-------|
| GET    | /api/maintenance/                        | Landlord (own), Tenant (own) | filter by ?status=&priority= |
| POST   | /api/maintenance/                        | Tenant   | create (own tenancy only) |
| GET    | /api/maintenance/{id}/                   | Landlord (own), Tenant (own) | detail |
| PATCH  | /api/maintenance/{id}/status/             | Landlord | Open → In Progress → Completed |
| POST   | /api/maintenance/{id}/cancel/             | Tenant (own, if Open), Landlord (own, any) | |

## Docs
| Method | Endpoint       | Notes |
|--------|----------------|-------|
| GET    | /api/schema/    | drf-spectacular OpenAPI schema |
| GET    | /api/docs/      | Swagger UI |

## Not in MVP (future phases)
- `/api/notifications/...` — Phase 11
- `/api/analytics/...` — Phase 11
- `/api/audit/...` — Phase 11
- `/api/organizations/...` — Phase 11 (multi-tenancy)