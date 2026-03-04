// Copyright (c) 2024, PG Management and contributors
// For license information, please see license.txt

frappe.ui.form.on('PG Payment', {
    refresh: function (frm) {
        // Add a custom button to print rent receipt
        if (!frm.is_new() && frm.doc.status === 'Paid') {
            frm.add_custom_button(__('Print Rent Receipt'), function () {
                frappe.set_route('print', 'PG Payment', frm.doc.name, 'PG Rent Receipt');
            }, __('Actions'));
        }

        // Set default year
        if (frm.is_new() && !frm.doc.payment_for_year) {
            frm.set_value('payment_for_year', new Date().getFullYear());
        }

        // Set default month
        if (frm.is_new() && !frm.doc.payment_for_month) {
            var months = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'];
            frm.set_value('payment_for_month', months[new Date().getMonth()]);
        }
    },

    pg_tenant: function (frm) {
        // Auto-fetch active room and mess bookings for this tenant
        if (frm.doc.pg_tenant) {
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'PG Room Booking',
                    filters: { pg_tenant: frm.doc.pg_tenant, status: 'Approved' },
                    fields: ['name', 'room_name', 'price'],
                    limit_page_length: 1
                },
                callback: function (r) {
                    if (r.message && r.message.length > 0) {
                        frm.set_value('room_booking', r.message[0].name);
                        frm.set_value('rent_amount', r.message[0].price);
                    }
                }
            });

            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'PG Mess Booking',
                    filters: { pg_tenant: frm.doc.pg_tenant, status: 'Approved' },
                    fields: ['name', 'mess_name', 'price'],
                    limit_page_length: 1
                },
                callback: function (r) {
                    if (r.message && r.message.length > 0) {
                        frm.set_value('mess_booking', r.message[0].name);
                        frm.set_value('mess_amount', r.message[0].price);
                    }
                }
            });
        }
    },

    rent_amount: function (frm) { calculate_total(frm); },
    mess_amount: function (frm) { calculate_total(frm); },
    deposit_amount: function (frm) { calculate_total(frm); },
    maintenance_amount: function (frm) { calculate_total(frm); },
    other_amount: function (frm) { calculate_total(frm); },
    paid_amount: function (frm) { calculate_total(frm); },
});

function calculate_total(frm) {
    var total = flt(frm.doc.rent_amount) + flt(frm.doc.mess_amount) +
        flt(frm.doc.deposit_amount) + flt(frm.doc.maintenance_amount) +
        flt(frm.doc.other_amount);

    if (total > 0) {
        frm.set_value('total_amount', total);
        frm.set_value('amount', total);
    }

    var outstanding = flt(frm.doc.total_amount || frm.doc.amount) - flt(frm.doc.paid_amount);
    frm.set_value('outstanding_amount', outstanding);

    // Auto-set status
    if (flt(frm.doc.paid_amount) >= flt(frm.doc.total_amount) && flt(frm.doc.total_amount) > 0) {
        frm.set_value('status', 'Paid');
    } else if (flt(frm.doc.paid_amount) > 0) {
        frm.set_value('status', 'Partially Paid');
    }
}
