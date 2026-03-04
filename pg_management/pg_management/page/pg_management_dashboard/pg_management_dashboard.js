frappe.pages['pg-management-dashboard'].on_page_load = function (wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'PG Management Dashboard',
        single_column: true
    });

    page.main.html(`
        <div class="pg-dashboard" style="padding: 15px;">
            <!-- Stats Cards Row 1 -->
            <div class="row" id="stats-row-1" style="margin-bottom: 20px;"></div>
            <!-- Stats Cards Row 2 -->
            <div class="row" id="stats-row-2" style="margin-bottom: 20px;"></div>
            <!-- Charts Row -->
            <div class="row" style="margin-bottom: 20px;">
                <div class="col-md-8">
                    <div class="card" style="border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                        <div class="card-body" style="padding: 20px;">
                            <h5 style="font-weight: 600; color: #333; margin-bottom: 15px;">Monthly Revenue (Last 12 Months)</h5>
                            <div id="revenue-chart" style="height: 280px;"></div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card" style="border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                        <div class="card-body" style="padding: 20px;">
                            <h5 style="font-weight: 600; color: #333; margin-bottom: 15px;">Payment Type Distribution</h5>
                            <div id="payment-chart" style="height: 280px;"></div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Quick Links -->
            <div class="row">
                <div class="col-12">
                    <div class="card" style="border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                        <div class="card-body" style="padding: 20px;">
                            <h5 style="font-weight: 600; color: #333; margin-bottom: 15px;">Quick Actions</h5>
                            <div class="row" id="quick-links"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `);

    // Load dashboard data
    load_dashboard(page);
};

frappe.pages['pg-management-dashboard'].refresh = function (wrapper) {
    load_dashboard();
};

function load_dashboard() {
    // Load stats
    frappe.call({
        method: 'pg_management.pg_management.api.get_pg_dashboard_data',
        callback: function (r) {
            if (r.message) {
                render_stats(r.message);
            }
        }
    });

    // Load revenue chart
    frappe.call({
        method: 'pg_management.pg_management.api.get_monthly_revenue_chart',
        callback: function (r) {
            if (r.message) {
                render_revenue_chart(r.message);
            }
        }
    });

    // Load payment distribution
    frappe.call({
        method: 'pg_management.pg_management.api.get_payment_type_distribution',
        callback: function (r) {
            if (r.message) {
                render_payment_chart(r.message);
            }
        }
    });

    // Render quick links
    render_quick_links();
}

function render_stats(data) {
    var cards_row1 = [
        {
            label: 'Total Tenants',
            value: data.total_tenants || 0,
            color: '#2490EF',
            icon: 'users',
            link: '/app/pg-tenant'
        },
        {
            label: 'Available Rooms',
            value: data.available_rooms || 0,
            color: '#29CD42',
            icon: 'home',
            link: '/app/pg-room?status=Available'
        },
        {
            label: 'Available Beds',
            value: data.available_beds || 0,
            color: '#00BCD4',
            icon: 'activity',
            link: '/app/pg-room'
        },
        {
            label: 'Bed Occupancy',
            value: (data.bed_occupancy_rate || 0) + '%',
            color: '#FF9800',
            icon: 'bar-chart-2',
            link: '/app/pg-room'
        }
    ];

    var cards_row2 = [
        {
            label: 'Pending Bookings',
            value: data.pending_room_bookings || 0,
            color: '#FF6F00',
            icon: 'clock',
            link: '/app/pg-room-booking?status=Pending'
        },
        {
            label: 'Overdue Payments',
            value: data.overdue_payments || 0,
            color: '#E53935',
            icon: 'alert-circle',
            link: '/app/pg-payment?status=Overdue'
        },
        {
            label: 'Monthly Revenue',
            value: format_currency(data.monthly_revenue || 0),
            color: '#7C4DFF',
            icon: 'trending-up',
            link: '/app/pg-payment?status=Paid'
        },
        {
            label: 'Open Tickets',
            value: data.open_tickets || 0,
            color: '#FF5722',
            icon: 'message-square',
            link: '/app/pg-ticket?status=Open'
        }
    ];

    $('#stats-row-1').html(cards_row1.map(card_html).join(''));
    $('#stats-row-2').html(cards_row2.map(card_html).join(''));
}

function card_html(card) {
    return `
        <div class="col-lg-3 col-md-6 col-sm-6 mb-3">
            <a href="${card.link}" style="text-decoration: none;">
                <div class="card" style="border-radius: 12px; border-left: 4px solid ${card.color};
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: transform 0.2s, box-shadow 0.2s;
                    cursor: pointer;" onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 4px 16px rgba(0,0,0,0.12)'"
                    onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 2px 8px rgba(0,0,0,0.08)'">
                    <div class="card-body" style="padding: 18px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-size: 12px; color: #8d99a6; text-transform: uppercase;
                                    letter-spacing: 0.5px; font-weight: 600;">${card.label}</div>
                                <div style="font-size: 28px; font-weight: 700; color: ${card.color};
                                    margin-top: 4px;">${card.value}</div>
                            </div>
                            <div style="width: 48px; height: 48px; border-radius: 10px;
                                background: ${card.color}15; display: flex; align-items: center;
                                justify-content: center;">
                                <svg class="icon" style="width: 24px; height: 24px; stroke: ${card.color};">
                                    <use href="#icon-${card.icon}"></use>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
            </a>
        </div>
    `;
}

function render_revenue_chart(data) {
    if (data.labels && data.labels.length) {
        new frappe.Chart('#revenue-chart', {
            data: data,
            type: 'line',
            height: 250,
            colors: ['#7C4DFF'],
            lineOptions: {
                regionFill: 1,
                hideDots: 0
            },
            axisOptions: {
                xIsSeries: true
            }
        });
    } else {
        $('#revenue-chart').html('<div style="text-align:center;color:#8d99a6;padding:80px 0;">No payment data yet</div>');
    }
}

function render_payment_chart(data) {
    if (data.labels && data.labels.length) {
        new frappe.Chart('#payment-chart', {
            data: data,
            type: 'pie',
            height: 250,
            colors: ['#2490EF', '#29CD42', '#FF9800', '#E53935', '#7C4DFF']
        });
    } else {
        $('#payment-chart').html('<div style="text-align:center;color:#8d99a6;padding:80px 0;">No payment data yet</div>');
    }
}

function render_quick_links() {
    var links = [
        { label: 'New Tenant', icon: 'user-plus', link: '/app/pg-tenant/new', color: '#2490EF' },
        { label: 'New Room Booking', icon: 'plus-square', link: '/app/pg-room-booking/new', color: '#29CD42' },
        { label: 'New Mess Booking', icon: 'plus-square', link: '/app/pg-mess-booking/new', color: '#FF9800' },
        { label: 'Record Payment', icon: 'credit-card', link: '/app/pg-payment/new', color: '#7C4DFF' },
        { label: 'New Announcement', icon: 'bell', link: '/app/pg-announcement/new', color: '#00BCD4' },
        { label: 'View Tickets', icon: 'message-square', link: '/app/pg-ticket', color: '#FF5722' }
    ];

    $('#quick-links').html(links.map(function (link) {
        return `
            <div class="col-lg-2 col-md-4 col-sm-6 mb-3">
                <a href="${link.link}" style="text-decoration: none;">
                    <div style="text-align: center; padding: 20px 10px; border-radius: 10px;
                        background: ${link.color}08; border: 1px solid ${link.color}20;
                        transition: all 0.2s; cursor: pointer;"
                        onmouseover="this.style.background='${link.color}15';this.style.transform='translateY(-2px)'"
                        onmouseout="this.style.background='${link.color}08';this.style.transform='translateY(0)'">
                        <svg class="icon" style="width: 24px; height: 24px; stroke: ${link.color}; margin-bottom: 8px;">
                            <use href="#icon-${link.icon}"></use>
                        </svg>
                        <div style="font-size: 12px; font-weight: 600; color: #333;">${link.label}</div>
                    </div>
                </a>
            </div>
        `;
    }).join(''));
}

function format_currency(value) {
    if (value >= 10000000) {
        return '₹' + (value / 10000000).toFixed(1) + ' Cr';
    } else if (value >= 100000) {
        return '₹' + (value / 100000).toFixed(1) + ' L';
    } else if (value >= 1000) {
        return '₹' + (value / 1000).toFixed(1) + ' K';
    }
    return '₹' + value;
}
