# Copyright (c) 2024, PG Management and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class PGMessBooking(Document):
	def validate(self):
		self.validate_mess_availability()
		self.validate_duplicate_booking()

	def validate_mess_availability(self):
		"""Check if the selected mess is available."""
		mess_status = frappe.db.get_value("PG Mess", self.mess, "status")
		if mess_status == "Not Available":
			frappe.throw(_("Mess {0} is currently not available").format(self.mess))

	def validate_duplicate_booking(self):
		"""Prevent duplicate active mess bookings for the same tenant."""
		if self.status in ("Pending", "Approved"):
			existing = frappe.db.exists(
				"PG Mess Booking",
				{
					"pg_tenant": self.pg_tenant,
					"status": ["in", ["Pending", "Approved"]],
					"name": ["!=", self.name],
				},
			)
			if existing:
				frappe.throw(
					_("Tenant {0} already has an active mess booking: {1}").format(
						self.pg_tenant, existing
					)
				)
