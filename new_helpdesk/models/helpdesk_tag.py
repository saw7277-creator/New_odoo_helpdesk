from odoo import fields, models

class HelpdeskTag(models.Model):
    _name = "helpdesk.tag"
    _description = "Helpdesk Tag"
    _order = "name"

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color Index")
