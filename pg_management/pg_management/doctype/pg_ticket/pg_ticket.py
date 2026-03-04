# Copyright (c) 2024, PG Management and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class PGTicket(Document):
	def validate(self):
		self.update_status_on_reply()

	def update_status_on_reply(self):
		"""Automatically update status to Replied when a reply is added."""
		if self.replies and len(self.replies) > 0 and self.status == "Open":
			self.status = "Replied"
