# Copyright (c) 2024, PG Management and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


# ─── Verhoeff Algorithm Tables ────────────────────────────────────────────────
# Used by UIDAI (Aadhaar) for checksum validation
# Reference: https://en.wikipedia.org/wiki/Verhoeff_algorithm

# Multiplication table 'd'
VERHOEFF_TABLE_D = [
	[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
	[1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
	[2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
	[3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
	[4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
	[5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
	[6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
	[7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
	[8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
	[9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]

# Permutation table 'p'
VERHOEFF_TABLE_P = [
	[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
	[1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
	[5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
	[8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
	[9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
	[4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
	[2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
	[7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]

# Inverse table 'inv'
VERHOEFF_TABLE_INV = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]


def verhoeff_checksum(number_str):
	"""
	Validate a number string using the Verhoeff checksum algorithm.
	Returns True if the checksum is valid (remainder is 0).

	This is the same algorithm used by UIDAI to validate Aadhaar numbers.
	"""
	c = 0
	# Process digits from right to left
	reversed_digits = [int(d) for d in reversed(number_str)]
	for i, digit in enumerate(reversed_digits):
		c = VERHOEFF_TABLE_D[c][VERHOEFF_TABLE_P[i % 8][digit]]
	return c == 0


def validate_aadhaar_format(aadhaar_number):
	"""
	Validate Aadhaar number format:
	1. Must be exactly 12 digits
	2. Must not start with 0 or 1
	3. Must not be all same digits (e.g. 222222222222)
	4. Must pass Verhoeff checksum
	Returns (is_valid, error_message)
	"""
	# Remove any spaces or dashes
	cleaned = aadhaar_number.replace(" ", "").replace("-", "")

	# Check: must be digits only
	if not cleaned.isdigit():
		return False, _("Aadhaar number must contain only digits")

	# Check: must be exactly 12 digits
	if len(cleaned) != 12:
		return False, _("Aadhaar number must be exactly 12 digits. Got {0} digits").format(
			len(cleaned)
		)

	# Check: must not start with 0 or 1
	if cleaned[0] in ("0", "1"):
		return False, _("Aadhaar number cannot start with 0 or 1")

	# Check: must not be all same digits
	if len(set(cleaned)) == 1:
		return False, _("Aadhaar number cannot be all same digits")

	# Check: Verhoeff checksum
	if not verhoeff_checksum(cleaned):
		return False, _("Aadhaar number failed checksum validation. Please verify the number")

	return True, None


class PGTenant(Document):
	def validate(self):
		self.validate_aadhaar()
		self.check_duplicate_aadhaar()

	def validate_aadhaar(self):
		"""Validate Aadhaar number format and checksum."""
		if not self.aadhaar_number:
			return

		# Clean the number (remove spaces/dashes for storage)
		self.aadhaar_number = self.aadhaar_number.replace(" ", "").replace("-", "")

		is_valid, error_message = validate_aadhaar_format(self.aadhaar_number)

		if is_valid:
			self.aadhaar_validation_status = "Valid"
		else:
			self.aadhaar_validation_status = "Invalid"
			frappe.throw(
				_("Aadhaar Validation Failed: {0}").format(error_message),
				title=_("Invalid Aadhaar Number"),
			)

	def check_duplicate_aadhaar(self):
		"""Ensure no other tenant has the same Aadhaar number."""
		if not self.aadhaar_number:
			return

		existing = frappe.db.exists(
			"PG Tenant",
			{
				"aadhaar_number": self.aadhaar_number,
				"name": ["!=", self.name],
			},
		)
		if existing:
			frappe.throw(
				_("Aadhaar number {0} is already registered with tenant {1}").format(
					self.aadhaar_number, existing
				),
				title=_("Duplicate Aadhaar Number"),
			)
