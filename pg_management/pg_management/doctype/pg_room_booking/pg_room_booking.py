# Copyright (c) 2024, PG Management and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class PGRoomBooking(Document):
	def validate(self):
		self.validate_room_availability()
		self.validate_duplicate_booking()

	def validate_room_availability(self):
		"""Check if the selected room is available."""
		room_status = frappe.db.get_value("PG Room", self.room, "status")
		if room_status == "Not Available":
			frappe.throw(_("Room {0} is currently not available").format(self.room))

	def validate_duplicate_booking(self):
		"""Prevent duplicate active bookings for the same tenant."""
		if self.status in ("Pending", "Approved"):
			existing = frappe.db.exists(
				"PG Room Booking",
				{
					"tenant": self.tenant,
					"status": ["in", ["Pending", "Approved"]],
					"name": ["!=", self.name],
				},
			)
			if existing:
				frappe.throw(
					_("Tenant {0} already has an active room booking: {1}").format(
						self.tenant, existing
					)
				)

	def on_update(self):
		"""Update room availability when booking is approved."""
		if self.status == "Approved":
			frappe.db.set_value("PG Room", self.room, "status", "Not Available")
		elif self.status == "Cancelled":
			# Check if any other active booking exists for this room
			other_booking = frappe.db.exists(
				"PG Room Booking",
				{
					"room": self.room,
					"status": "Approved",
					"name": ["!=", self.name],
				},
			)
			if not other_booking:
				frappe.db.set_value("PG Room", self.room, "status", "Available")
