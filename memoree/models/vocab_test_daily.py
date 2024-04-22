from odoo import api, fields, models, _
from .utils import tinh_do_tuong_dong


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
    simular_ratio = fields.Float()
    maximum_similarity_ratio = fields.Float(related='vocab_test_id.maximum_similarity_ratio')
    check_type = fields.Selection(related='vocab_test_id.check_type')


    @api.onchange('value_input')
    def onchange_value_input(self):
        for rec in self:
            if rec.value_input:
                status = 'failed'
                simular_ratio = 0
                value_input = rec.value_input.strip().lower().strip(".")
                value_exactly = rec.value.strip().lower().strip(".")
                if rec.vocab_test_id.check_type == 'have_similarity':
                    simular_ratio = round(tinh_do_tuong_dong(value_input, value_exactly), 2)
                    if simular_ratio >= rec.maximum_similarity_ratio:
                        status = 'passed'
                else:
                    if value_input == value_exactly:
                        status = 'passed'

                rec.status = status
                rec.simular_ratio = simular_ratio

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
        simular_ratio = 0
        value_input = self.value_input.strip().lower().strip(".")
        value_exactly = self.value.strip().lower().strip(".")
        if self.vocab_test_id.check_type == 'have_similarity':
            simular_ratio = round(tinh_do_tuong_dong(value_input, value_exactly), 2)
            if simular_ratio >= self.maximum_similarity_ratio:
                status = 'passed'
        else:
            if value_input == value_exactly:
                status = 'passed'

        self.status = status
        self.simular_ratio = simular_ratio

    def action_mark_hard(self):
        self.sudo().vocab_import_id.is_hard = True

    def action_unmark_hard(self):
        self.sudo().vocab_import_id.is_hard = False

    def action_reset(self):
        self.sudo().write({'status': False, 'value_input': '', 'simular_ratio': 0})
