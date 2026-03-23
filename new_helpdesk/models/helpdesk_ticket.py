from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "Helpdesk Ticket"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "priority desc, id desc"
    _rec_name = "display_name"

    name = fields.Char(string="Subject", required=True, tracking=True)
    display_name = fields.Char(compute="_compute_display_name", store=True, readonly=True)
    ticket_number = fields.Char(string="Ticket #", default=lambda self: _("New"), copy=False, readonly=True)
    active = fields.Boolean(default=True)
    team_id = fields.Many2one("helpdesk.team", required=True, tracking=True, ondelete="cascade")
    stage_id = fields.Many2one("helpdesk.stage", string="Stage", tracking=True, group_expand="_read_group_stage_ids", ondelete="set null")
    user_id = fields.Many2one("res.users", string="Assigned to", tracking=True, ondelete="set null")
    partner_id = fields.Many2one("res.partner", string="Customer", tracking=True, ondelete="set null")
    contact_name = fields.Char()
    email = fields.Char()
    phone = fields.Char()
    priority = fields.Selection([("0", "Low"), ("1", "Normal"), ("2", "High"), ("3", "Urgent")], default="1", tracking=True)
    description = fields.Html()
    due_date = fields.Date()
    tag_ids = fields.Many2many("helpdesk.tag", string="Tags")
    closed_date = fields.Datetime(readonly=True)

    @api.depends("ticket_number", "name")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.ticket_number} - {rec.name}" if rec.ticket_number and rec.ticket_number != _("New") else (rec.name or "")

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env["ir.sequence"]
        for vals in vals_list:
            if vals.get("ticket_number", _("New")) == _("New"):
                vals["ticket_number"] = seq.next_by_code("helpdesk.ticket") or _("New")
        records = super().create(vals_list)
        for rec in records:
            if not rec.stage_id:
                stage = self.env["helpdesk.stage"].search(["|", ("team_ids", "=", False), ("team_ids", "in", rec.team_id.id)], order="sequence,id", limit=1)
                if stage:
                    rec.stage_id = stage
        return records

    def write(self, vals):
        res = super().write(vals)
        if "stage_id" in vals:
            for rec in self:
                if rec.stage_id.fold and not rec.closed_date:
                    rec.closed_date = fields.Datetime.now()
                elif not rec.stage_id.fold:
                    rec.closed_date = False
        return res

    @api.constrains("stage_id", "team_id")
    def _check_stage_team(self):
        for rec in self:
            if rec.stage_id and rec.stage_id.team_ids and rec.team_id not in rec.stage_id.team_ids:
                raise ValidationError(_("Selected stage does not belong to this Helpdesk Team."))

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        team_id = self.env.context.get("default_team_id")
        stage_domain = []
        if team_id:
            stage_domain = ["|", ("team_ids", "=", False), ("team_ids", "in", [team_id])]
        return self.env["helpdesk.stage"].search(stage_domain, order="sequence, id")
