# Permissions Matrix

Scope rule that applies everywhere below: "own" means scoped through ownership —
a Landlord only ever sees Properties they own, Units under those Properties,
Tenancies on those Units, and Rent/Payment/Maintenance records tied to those
Tenancies. A Tenant only ever sees their own Tenancy and records tied to it.
This scoping is enforced in querysets/services (see clean-code Section 5 of the
roadmap doc), never trusted from the frontend alone.

| Action                                   | Landlord            | Tenant                  | Admin (future) |
|-------------------------------------------|----------------------|--------------------------|----------------|
| Register / Login / Refresh token          | ✅                   | ✅                       | ✅             |
| View / edit own profile                   | ✅ (own)             | ✅ (own)                 | ✅ (any)       |
| Create Property                           | ✅                   | ❌                       | ✅             |
| View Property                             | ✅ (own)             | ❌ (indirect, via Unit)  | ✅ (any)       |
| Edit / Delete Property                    | ✅ (own)             | ❌                       | ✅             |
| Create Unit under Property                | ✅ (own property)    | ❌                       | ✅             |
| View Unit                                 | ✅ (own)             | ✅ (own assigned unit)   | ✅ (any)       |
| Edit / Delete Unit                        | ✅ (own)             | ❌                       | ✅             |
| Invite / add Tenant                       | ✅                   | ❌                       | ✅             |
| View Tenant list                          | ✅ (own tenants)     | ❌                       | ✅ (any)       |
| View own Tenant profile                   | ✅ (own tenants)     | ✅ (self)                | ✅             |
| Create Tenancy (assign tenant → unit)     | ✅                   | ❌                       | ✅             |
| End / update Tenancy                      | ✅ (own)             | ❌                       | ✅             |
| View Tenancy                              | ✅ (own)             | ✅ (own)                 | ✅ (any)       |
| Generate / view Rent Records              | ✅ (own tenants)     | ✅ (own only)            | ✅ (any)       |
| Update Rent Record status (mark paid etc.)| ✅ (own)             | ❌                       | ✅             |
| Upload payment proof                      | ❌                   | ✅ (own rent record)     | ❌             |
| Verify a Payment                          | ✅ (own)             | ❌                       | ✅             |
| View Payment history                      | ✅ (own tenants)     | ✅ (own only)            | ✅ (any)       |
| Create Maintenance Request                | ❌                   | ✅ (own tenancy)         | ❌             |
| View Maintenance Requests                 | ✅ (own properties)  | ✅ (own only)            | ✅ (any)       |
| Update Maintenance Request status         | ✅ (own)             | ❌                       | ✅             |
| Cancel own Maintenance Request            | ✅ (own, any status) | ✅ (own, only if "Open") | ✅             |
| View analytics / reports                  | ✅ (own data) *future*| ❌                      | ✅ (platform-wide) *future* |
| Manage users / platform settings          | ❌                   | ❌                       | ✅ *future*    |

## Notes for implementation
- Enforce these with a permission class per app (`IsLandlord`, `IsTenant`,
  `IsOwnerLandlord`, `IsAssignedTenant`) plus ownership-scoped querysets
  (`Property.objects.for_landlord(user)`), not just `IsAuthenticated`.
- "Own" scoping must hold even for nested resources — e.g. a Landlord requesting
  `/api/rent/42/` should get a 404 (not 403) if that rent record isn't tied to
  one of their properties, to avoid leaking existence of other landlords' data.
- Admin role permissions are listed now for completeness but are **not
  implemented in the MVP** — no Admin views/permissions get built until Phase 11.
