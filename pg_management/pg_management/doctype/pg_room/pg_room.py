# Copyright (c) 2024, PG Management and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cint


class PGRoom(Document):
	def validate(self):
		self.validate_beds()
		self.calculate_price_per_bed()
		self.update_bed_counts()

	def validate_beds(self):
		"""Ensure total beds is at least 1."""
		if cint(self.total_beds) < 1:
			frappe.throw(_("Total Beds must be at least 1"))

	def calculate_price_per_bed(self):
		"""Auto-calculate price per bed if not manually set."""
		if not self.price_per_bed or flt(self.price_per_bed) == 0:
			if cint(self.total_beds) > 0:
				self.price_per_bed = flt(self.price) / cint(self.total_beds)

	def update_bed_counts(self):
		"""Update occupied and available bed counts from active bookings."""
		occupied = frappe.db.count(
			"PG Room Booking",
			{"room": self.name, "status": "Approved"},
		)
		self.occupied_beds = cint(occupied)
		self.available_beds = cint(self.total_beds) - self.occupied_beds
		self.occupancy_status = f"{self.occupied_beds}/{self.total_beds} beds occupied"

		# Auto-update status based on occupancy
		if self.occupied_beds >= cint(self.total_beds):
			self.status = "Fully Occupied"
		elif self.occupied_beds > 0:
			self.status = "Partially Occupied"
		else:
			self.status = "Available"


def update_room_occupancy(room_name):
	"""
	Utility function to recalculate and save room occupancy.
	Called from PG Room Booking on_update.
	"""
	room = frappe.get_doc("PG Room", room_name)
	occupied = frappe.db.count(
		"PG Room Booking",
		{"room": room_name, "status": "Approved"},
	)
	room.occupied_beds = cint(occupied)
	room.available_beds = cint(room.total_beds) - room.occupied_beds
	room.occupancy_status = f"{room.occupied_beds}/{room.total_beds} beds occupied"

	if room.occupied_beds >= cint(room.total_beds):
		room.status = "Fully Occupied"
	elif room.occupied_beds > 0:
		room.status = "Partially Occupied"
	else:
		room.status = "Available"

	room.db_set("occupied_beds", room.occupied_beds)
	room.db_set("available_beds", room.available_beds)
	room.db_set("occupancy_status", room.occupancy_status)
	room.db_set("status", room.status)
