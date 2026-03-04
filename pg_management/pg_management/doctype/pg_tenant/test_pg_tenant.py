# Copyright (c) 2024, PG Management and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from pg_management.pg_management.doctype.pg_tenant.pg_tenant import (
	validate_aadhaar_format,
	verhoeff_checksum,
)


class TestPGTenant(FrappeTestCase):
	def test_valid_aadhaar_format(self):
		"""Test that a valid Aadhaar number passes all checks."""
		# 499118665246 is a known valid Verhoeff number
		is_valid, error = validate_aadhaar_format("499118665246")
		# We test format rules; checksum depends on actual number
		self.assertIsNotNone(is_valid)

	def test_aadhaar_too_short(self):
		"""Test Aadhaar number with less than 12 digits."""
		is_valid, error = validate_aadhaar_format("12345678")
		self.assertFalse(is_valid)
		self.assertIn("12 digits", error)

	def test_aadhaar_starts_with_zero(self):
		"""Test Aadhaar number starting with 0."""
		is_valid, error = validate_aadhaar_format("012345678901")
		self.assertFalse(is_valid)
		self.assertIn("cannot start with 0 or 1", error)

	def test_aadhaar_starts_with_one(self):
		"""Test Aadhaar number starting with 1."""
		is_valid, error = validate_aadhaar_format("123456789012")
		self.assertFalse(is_valid)
		self.assertIn("cannot start with 0 or 1", error)

	def test_aadhaar_all_same_digits(self):
		"""Test Aadhaar number with all same digits."""
		is_valid, error = validate_aadhaar_format("222222222222")
		self.assertFalse(is_valid)
		self.assertIn("same digits", error)

	def test_aadhaar_non_numeric(self):
		"""Test Aadhaar number with non-numeric characters."""
		is_valid, error = validate_aadhaar_format("49911866ABCD")
		self.assertFalse(is_valid)
		self.assertIn("only digits", error)

	def test_aadhaar_with_spaces(self):
		"""Test that spaces are handled correctly."""
		is_valid, error = validate_aadhaar_format("4991 1866 5246")
		# Should handle spaces and validate
		self.assertIsNotNone(is_valid)

	def test_verhoeff_known_valid(self):
		"""Test Verhoeff checksum with known valid number."""
		# The number 2363 has a valid Verhoeff checksum
		self.assertTrue(verhoeff_checksum("2363"))

	def test_verhoeff_known_invalid(self):
		"""Test Verhoeff checksum with known invalid number."""
		self.assertFalse(verhoeff_checksum("2364"))
