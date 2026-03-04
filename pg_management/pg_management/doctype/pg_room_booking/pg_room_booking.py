# Copyright (c) 2024, PG Management and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class PGRoomBooking(Document):
	def validate(self):
		self.validate_bed_availability()
		self.validate_duplicate_booking()
		self.auto_assign_bed_number()

	def validate_bed_availability(self):
		"""Check if the selected room has available beds."""
		if self.status not in ("Pending", "Approved"):
			return

		room = frappe.get_doc("PG Room", self.room)
		total_beds = cint(room.total_beds)

		# Count current approved bookings for this room (excluding this one)
		current_occupants = frappe.db.count(
			"PG Room Booking",
			{
				"room": self.room,
				"status": "Approved",
				"name": ["!=", self.name],
			},
		)

		# Also count pending bookings if this booking is being approved
		if self.status == "Approved":
			available_beds = total_beds - cint(current_occupants)
			if available_beds <= 0:
				frappe.throw(
					_("Room {0} has no available beds. All {1} beds are occupied.").format(
						self.room, total_beds
					),
					title=_("No Beds Available"),
				)

	def validate_duplicate_booking(self):
		"""Prevent duplicate active bookings for the same tenant."""
		if self.status in ("Pending", "Approved"):
			existing = frappe.db.exists(
				"PG Room Booking",
				{
					"pg_tenant": self.pg_tenant,
					"status": ["in", ["Pending", "Approved"]],
					"name": ["!=", self.name],
				},
			)
			if existing:
				frappe.throw(
					_("Tenant {0} already has an active room booking: {1}").format(
						self.pg_tenant, existing
					)
				)

	def auto_assign_bed_number(self):
		"""Auto-assign bed number if not set and booking is approved."""
		if self.status == "Approved" and not self.bed_number:
			room = frappe.get_doc("PG Room", self.room)
			total_beds = cint(room.total_beds)

			# Get all bed numbers already taken in this room
			taken_beds = frappe.get_all(
				"PG Room Booking",
				filters={
					"room": self.room,
					"status": "Approved",
					"name": ["!=", self.name],
					"bed_number": [">", 0],
				},
				pluck="bed_number",
			)

			# Find the first available bed number
			for bed_num in range(1, total_beds + 1):
				if bed_num not in taken_beds:
					self.bed_number = bed_num
					break

	def on_update(self):
		"""Update room bed occupancy when booking status changes."""
		self.update_room_occupancy()

	def on_trash(self):
		"""Update room bed occupancy when booking is deleted."""
		self.update_room_occupancy()

	def update_room_occupancy(self):
		"""Recalculate room occupancy after booking changes."""
		if self.room:
			from pg_management.pg_management.doctype.pg_room.pg_room import (
				update_room_occupancy,
			)
			update_room_occupancy(self.room)
