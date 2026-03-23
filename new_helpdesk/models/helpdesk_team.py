from odoo import api, fields, models

class HelpdeskTeam(models.Model):
    _name = "helpdesk.team"
    _description = "Helpdesk Team"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    name = fields.Char(string="Team Name", required=True, tracking=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    email_alias = fields.Char(string="Email Alias", tracking=True)
    color = fields.Integer()
    member_ids = fields.Many2many("res.users", string="Members")
    ticket_ids = fields.One2many("helpdesk.ticket", "team_id", string="Tickets")
    ticket_count = fields.Integer(compute="_compute_counts")
    open_count = fields.Integer(compute="_compute_counts")
    unassigned_count = fields.Integer(compute="_compute_counts")
    urgent_count = fields.Integer(compute="_compute_counts")
    waiting_count = fields.Integer(compute="_compute_counts")
    overdue_count = fields.Integer(compute="_compute_counts")
    closed_count = fields.Integer(compute="_compute_counts")

    @api.depends("ticket_ids", "ticket_ids.stage_id", "ticket_ids.user_id", "ticket_ids.priority", "ticket_ids.due_date")
    def _compute_counts(self):
        today = fields.Date.today()
        for team in self:
            tickets = team.ticket_ids
            team.ticket_count = len(tickets)
            team.open_count = len(tickets.filtered(lambda t: not t.stage_id.fold))
            team.unassigned_count = len(tickets.filtered(lambda t: not t.user_id and not t.stage_id.fold))
            team.urgent_count = len(tickets.filtered(lambda t: t.priority == "3" and not t.stage_id.fold))
            team.waiting_count = len(tickets.filtered(lambda t: t.stage_id and t.stage_id.is_waiting and not t.stage_id.fold))
            team.overdue_count = len(tickets.filtered(lambda t: t.due_date and t.due_date < today and not t.stage_id.fold))
            team.closed_count = len(tickets.filtered(lambda t: t.stage_id.fold))

    def action_view_tickets(self):
        self.ensure_one()
        action = self.env.ref("new_helpdesk.action_helpdesk_ticket_all").read()[0]
        action["domain"] = [("team_id", "=", self.id)]
        action["context"] = {"default_team_id": self.id}
        return action
