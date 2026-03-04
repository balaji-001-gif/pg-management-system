# Copyright (c) 2024, PG Management and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import nowdate, getdate, flt, add_months


@frappe.whitelist()
def get_pg_dashboard_data():
	"""Get dashboard summary data for PG Management."""
	data = {}

	# --- Tenant Stats ---
	data["total_tenants"] = frappe.db.count("PG Tenant")

	# --- Room Stats ---
	data["total_rooms"] = frappe.db.count("PG Room")
	data["available_rooms"] = frappe.db.count("PG Room", {"status": "Available"})
	data["occupied_rooms"] = frappe.db.count("PG Room", {"status": "Not Available"})
	data["occupancy_rate"] = (
		round((data["occupied_rooms"] / data["total_rooms"]) * 100, 1)
		if data["total_rooms"] > 0
		else 0
	)

	# --- Mess Stats ---
	data["total_mess"] = frappe.db.count("PG Mess")
	data["active_mess_bookings"] = frappe.db.count(
		"PG Mess Booking", {"status": "Approved"}
	)

	# --- Booking Stats ---
	data["pending_room_bookings"] = frappe.db.count(
		"PG Room Booking", {"status": "Pending"}
	)
	data["approved_room_bookings"] = frappe.db.count(
		"PG Room Booking", {"status": "Approved"}
	)
	data["pending_mess_bookings"] = frappe.db.count(
		"PG Mess Booking", {"status": "Pending"}
	)

	# --- Payment Stats ---
	today = nowdate()
	current_month_start = getdate(today).replace(day=1)

	data["total_revenue"] = (
		frappe.db.get_value(
			"PG Payment",
			{"status": "Paid"},
			"sum(amount)",
		)
		or 0
	)

	data["monthly_revenue"] = (
		frappe.db.get_value(
			"PG Payment",
			{"status": "Paid", "payment_date": [">=", current_month_start]},
			"sum(amount)",
		)
		or 0
	)

	data["total_outstanding"] = (
		frappe.db.get_value(
			"PG Payment",
			{"status": ["in", ["Partially Paid", "Overdue"]]},
			"sum(outstanding_amount)",
		)
		or 0
	)

	data["overdue_payments"] = frappe.db.count("PG Payment", {"status": "Overdue"})

	# --- Ticket Stats ---
	data["open_tickets"] = frappe.db.count("PG Ticket", {"status": "Open"})

	return data


@frappe.whitelist()
def get_monthly_revenue_chart():
	"""Get month-wise revenue data for the last 12 months."""
	today = getdate(nowdate())
	months = []
	revenue = []

	for i in range(11, -1, -1):
		month_date = add_months(today, -i)
		month_start = month_date.replace(day=1)
		if month_date.month == 12:
			month_end = month_date.replace(year=month_date.year + 1, month=1, day=1)
		else:
			month_end = month_date.replace(month=month_date.month + 1, day=1)

		month_revenue = (
			frappe.db.get_value(
				"PG Payment",
				{
					"status": "Paid",
					"payment_date": [">=", month_start],
					"payment_date": ["<", month_end],
				},
				"sum(amount)",
			)
			or 0
		)

		months.append(month_date.strftime("%b %Y"))
		revenue.append(flt(month_revenue))

	return {"labels": months, "datasets": [{"name": "Revenue", "values": revenue}]}


@frappe.whitelist()
def get_payment_type_distribution():
	"""Get payment distribution by type."""
	result = frappe.db.get_all(
		"PG Payment",
		filters={"status": ["in", ["Paid", "Partially Paid"]]},
		fields=["payment_type", "sum(amount) as total"],
		group_by="payment_type",
		order_by="total desc",
	)

	labels = [r.payment_type for r in result]
	values = [flt(r.total) for r in result]

	return {"labels": labels, "datasets": [{"name": "Amount", "values": values}]}
