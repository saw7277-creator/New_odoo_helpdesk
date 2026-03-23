from odoo import fields, models

class HelpdeskSLAPolicy(models.Model):
    _name = "helpdesk.sla.policy"
    _description = "Helpdesk SLA Policy"
    _order = "name"

    name = fields.Char(string="SLA Name", required=True)
    team_id = fields.Many2one("helpdesk.team", string="Helpdesk Team", required=True, ondelete="cascade")
    priority = fields.Selection([("0", "Low"), ("1", "Normal"), ("2", "High"), ("3", "Urgent")], default="1")
    reach_stage_id = fields.Many2one("helpdesk.stage", string="Reach Stage", ondelete="set null")
    within = fields.Integer(string="Response Time (Hours)", required=True)
