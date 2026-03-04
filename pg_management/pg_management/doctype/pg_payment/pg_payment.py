# Copyright (c) 2024, PG Management and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, getdate, flt


class PGPayment(Document):
	def validate(self):
		self.calculate_totals()
		self.set_receipt_number()
		self.set_payment_status()

	def calculate_totals(self):
		"""Calculate total amount from breakdown fields."""
		self.total_amount = flt(
			flt(self.rent_amount)
			+ flt(self.mess_amount)
			+ flt(self.deposit_amount)
			+ flt(self.maintenance_amount)
			+ flt(self.other_amount)
		)

		# If breakdown is not used, use the main amount field
		if self.total_amount == 0:
			self.total_amount = flt(self.amount)

		# Sync main amount with total
		if self.total_amount > 0:
			self.amount = self.total_amount

		# Calculate outstanding
		self.outstanding_amount = flt(self.total_amount) - flt(self.paid_amount)

	def set_receipt_number(self):
		"""Auto-generate receipt number if not set."""
		if not self.receipt_number and self.status == "Paid":
			self.receipt_number = self.name

	def set_payment_status(self):
		"""Auto-set status based on paid vs total amounts."""
		if flt(self.paid_amount) <= 0 and self.status not in ("Draft", "Cancelled"):
			self.status = "Draft"
		elif flt(self.paid_amount) >= flt(self.total_amount) and flt(self.total_amount) > 0:
			self.status = "Paid"
			if not self.receipt_number:
				self.receipt_number = self.name
		elif flt(self.paid_amount) > 0 and flt(self.paid_amount) < flt(self.total_amount):
			self.status = "Partially Paid"

	def on_update(self):
		"""Set receipt number after save (name is available)."""
		if self.status == "Paid" and not self.receipt_number:
			self.receipt_number = self.name
			self.db_set("receipt_number", self.name)
