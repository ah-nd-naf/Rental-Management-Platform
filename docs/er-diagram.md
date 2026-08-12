# ER Diagram — Rental & Tenant Management Platform

This renders automatically as a diagram on GitHub/GitLab (mermaid). If your docs
viewer doesn't support mermaid, paste the block into https://mermaid.live to view it.

```mermaid
erDiagram
    USER ||--o{ PROPERTY : owns
    USER ||--|| TENANT_PROFILE : "has (if role=tenant)"
    PROPERTY ||--o{ UNIT : contains
    TENANT_PROFILE ||--o{ TENANCY : "holds"
    UNIT ||--o{ TENANCY : "assigned via"
    TENANCY ||--o{ RENT_RECORD : generates
    RENT_RECORD ||--o{ PAYMENT : "paid via"
    TENANCY ||--o{ MAINTENANCE_REQUEST : raises
    USER ||--o{ PAYMENT : verifies
    USER ||--o{ MAINTENANCE_REQUEST : updates

    USER {
        int id PK
        string email UK
        string password
        string role "landlord / tenant / admin"
        string first_name
        string last_name
        string phone
        datetime created_at
        datetime updated_at
    }
    PROPERTY {
        int id PK
        int owner_id FK "-> USER"
        string name
        string address
        text description
        datetime created_at
        datetime updated_at
    }
    UNIT {
        int id PK
        int property_id FK "-> PROPERTY"
        string unit_number
        int bedrooms
        decimal monthly_rent
        string status "available / occupied / maintenance / inactive"
        datetime created_at
        datetime updated_at
    }
    TENANT_PROFILE {
        int id PK
        int user_id FK "-> USER, one-to-one"
        string emergency_contact
        text notes
        datetime created_at
        datetime updated_at
    }
    TENANCY {
        int id PK
        int tenant_id FK "-> TENANT_PROFILE"
        int unit_id FK "-> UNIT"
        date lease_start
        date lease_end "nullable, open-ended if null"
        decimal rent_amount "snapshot at lease signing"
        int due_day "day of month rent is due"
        string status "pending / active / ended"
        datetime created_at
        datetime updated_at
    }
    RENT_RECORD {
        int id PK
        int tenancy_id FK "-> TENANCY"
        date month "first of the billed month"
        decimal amount
        date due_date
        string status "pending / paid / overdue / partially_paid / cancelled"
        datetime created_at
        datetime updated_at
    }
    PAYMENT {
        int id PK
        int rent_record_id FK "-> RENT_RECORD"
        decimal amount
        string proof_url "Cloudinary URL"
        date payment_date
        int verified_by_id FK "-> USER (landlord), nullable"
        datetime verified_at "nullable"
        string status "pending_verification / verified / rejected"
        datetime created_at
        datetime updated_at
    }
    MAINTENANCE_REQUEST {
        int id PK
        int tenancy_id FK "-> TENANCY"
        string title
        text description
        string priority "low / medium / high"
        string status "open / in_progress / completed / cancelled"
        datetime created_at
        datetime updated_at
    }
```

## Design decisions worth noting

1. **`TENANT_PROFILE` is separate from `USER`, one-to-one.** `USER` handles
   auth/role for everyone (landlord, tenant, future admin). `TENANT_PROFILE`
   holds tenant-only fields, keeping `users` app generic and `tenants` app
   domain-specific — matches the app-per-domain backend split.

2. **`TENANCY` is the join entity between tenant and unit — never a direct FK
   from `TENANT_PROFILE` to `UNIT`.** This is what makes move-outs, unit
   changes, and lease history possible without deleting/overwriting data,
   exactly as called out in the original spec.

3. **`rent_amount` is snapshotted on `TENANCY`, not read live from `UNIT`.**
   If a landlord changes a unit's listed rent later, existing tenants' locked-in
   rent shouldn't silently change — new tenancies pick up the current unit rent
   at signing time.

4. **`RENT_RECORD` is a monthly row generated from a `TENANCY`,** not something
   the tenant or landlord free-types each time — this is what
   `apps/rent/services.py` generates and updates (Phase 4 of the roadmap).

5. **`PAYMENT` is separate from `RENT_RECORD`** to support partial payments —
   one rent record can eventually have multiple payment rows summing toward it,
   and `verified_by`/`verified_at` gives you an audit trail of who confirmed it.

6. **No `ORGANIZATION` entity yet** — that's the Phase 11 multi-tenancy addition;
   when it lands, `PROPERTY.owner_id` conceptually moves under an org, but
   nothing above needs to be redesigned for it, just extended.
