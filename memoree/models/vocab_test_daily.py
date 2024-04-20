from odoo import api, fields, models, _


class VocabTestDaily(models.Model):
    _name = "vocab.test.daily"

    vocab_test_id = fields.Many2one('vocab.test')
    vocab_import_id = fields.Many2one('vocab.import', string="Name")
    name = fields.Char(related='vocab_import_id.name')
    value = fields.Char(related='vocab_import_id.value')
    is_hard = fields.Boolean(related='vocab_import_id.is_hard')
    value_input = fields.Char(default='')
    date = fields.Date()
    status = fields.Selection([('passed', 'Passed'), ('failed', 'Failed')])

    @api.onchange('value_input')
    def onchange_value_input(self):
        for rec in self:
            if rec.value_input:
                if rec.value_input.strip().lower().strip(".") == rec.value.strip().lower().strip("."):
                    rec.status = 'passed'
                else:
                    rec.status = 'failed'

    def action_hint(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'warning',
                'message': _(self.value),
            },
        }

    @api.onchange('status')
    def onchange_status(self):
        for rec in self:
            rec.status = rec.status

    def action_check(self):
        status = 'failed'
        if self.value_input.strip().lower().strip(".") == self.value.strip().lower().strip("."):
            status = 'passed'
        self.status = status

    def action_mark_hard(self):
        self.sudo().vocab_import_id.is_hard = True

    def action_unmark_hard(self):
        self.sudo().vocab_import_id.is_hard = False

    def action_reset(self):
        self.sudo().write({'status': False, 'value_input': ''})