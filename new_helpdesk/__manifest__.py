{
    "name": "New Helpdesk",
    "version": "18.0.1.0.0",
    "summary": "Custom Helpdesk app for Odoo 18 Community",
    "category": "Services/Helpdesk",
    "author": "OpenAI",
    "license": "LGPL-3",
    "depends": ["mail", "contacts"],
    "data": [
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",
        "data/helpdesk_sequence.xml",
        "data/helpdesk_stage_data.xml",
        "views/helpdesk_team_views.xml",
        "views/helpdesk_stage_views.xml",
        "views/helpdesk_tag_views.xml",
        "views/helpdesk_sla_views.xml",
        "views/helpdesk_ticket_views.xml",
        "views/helpdesk_menus.xml"
    ],
    "application": True,
    "installable": True
}
