# PG Management System

A Frappe/ERPNext v15 app for managing Paying Guest (PG) accommodations.

## Features

- **Room Management** – Add, edit, and track PG rooms with pricing, size, and availability
- **Mess Management** – Manage mess/food services with pricing and availability
- **Room Booking** – Tenants can book rooms; admins can approve/reject
- **Mess Booking** – Tenants can subscribe to mess; admins can approve/reject
- **Announcements** – Admins can post announcements visible to all tenants
- **Ticket System** – Tenants raise tickets; admins reply and close them

## Installation

```bash
# Get the app
bench get-app https://github.com/your-org/pg_management.git

# Install on your site
bench --site your-site.localhost install-app pg_management

# Run migration
bench --site your-site.localhost migrate
```

## Roles

| Role | Access |
|------|--------|
| **PG Admin** | Full access to all DocTypes |
| **PG Tenant** | Can view rooms/mess, create bookings & tickets |

## License

MIT
