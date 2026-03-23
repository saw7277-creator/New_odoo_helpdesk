from odoo import fields, models

class HelpdeskStage(models.Model):
    _name = "helpdesk.stage"
    _description = "Helpdesk Stage"
    _order = "sequence, id"

    name = fields.Char(string="Stage Name", required=True)
    sequence = fields.Integer(default=10)
    team_ids = fields.Many2many("helpdesk.team", string="Helpdesk Teams")
    fold = fields.Boolean(string="Folded in Kanban")
    is_waiting = fields.Boolean(string="Waiting Stage")
    color = fields.Integer()
