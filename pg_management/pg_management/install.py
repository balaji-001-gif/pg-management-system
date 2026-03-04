# Copyright (c) 2024, PG Management and contributors
# For license information, please see license.txt

import json
import os

import frappe
from frappe import _


def after_install():
	"""Create Number Cards and setup default data after install/migrate."""
	create_number_cards()
	create_custom_roles()


def create_number_cards():
	"""Create Number Card documents from fixture file."""
	fixture_path = os.path.join(
		os.path.dirname(__file__), "number_card.json"
	)

	if not os.path.exists(fixture_path):
		return

	with open(fixture_path, "r") as f:
		cards = json.load(f)

	for card_data in cards:
		card_name = card_data.get("name")
		if not frappe.db.exists("Number Card", card_name):
			try:
				doc = frappe.get_doc(card_data)
				doc.insert(ignore_permissions=True)
				frappe.db.commit()
			except Exception as e:
				frappe.log_error(
					f"Error creating Number Card '{card_name}': {str(e)}",
					"PG Management Setup",
				)


def create_custom_roles():
	"""Create PG Admin and PG Tenant roles if they don't exist."""
	for role_name in ["PG Admin", "PG Tenant"]:
		if not frappe.db.exists("Role", role_name):
			try:
				frappe.get_doc(
					{
						"doctype": "Role",
						"role_name": role_name,
						"desk_access": 1,
						"is_custom": 1,
					}
				).insert(ignore_permissions=True)
				frappe.db.commit()
			except Exception:
				pass
