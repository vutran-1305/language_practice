from odoo import api, fields, models
from datetime import datetime, date
from ast import literal_eval

class VocabTest(models.Model):
    _name = "vocab.test"
    _description = "Vocab Test"

    name = fields.Char()
    model_name = fields.Char(string='Model Name', default='vocab.import', store=True)
    domain = fields.Char(string="Filter",  readonly=False, store=True)
    start_time = fields.Date()
    end_time = fields.Date()
    is_limit = fields.Boolean()
    count_word = fields.Integer()
    vocab_test_daily_ids = fields.One2many('vocab.test.daily', 'vocab_test_id', domain=lambda self: [('create_uid', 'in', [self.env.user.id])])
    count_test_daily = fields.Integer()

    def action_start_test(self):
        daily_ids = self.env['vocab.test.daily'].sudo().search([('vocab_test_id', '=', self.id), ('date', '=', date.today()), ('create_uid', '=', self.create_uid.id)])
        if not daily_ids:
            if not self.domain:
                vocab_import = self.env['vocab.import'].sudo().search([])
            else:
                record_domain = literal_eval(self.domain or "[]")
                vocab_import = self.env['vocab.import'].sudo().search(record_domain)
            if vocab_import:
                values = []
                for vocab in vocab_import:
                    values.append({'vocab_import_id': vocab.id, 'date': date.today(), 'vocab_test_id': self.id})
                daily_ids = self.env['vocab.test.daily'].sudo().create(values)
        action = {
            'name': 'Test Daily - %s' % date.today().strftime("%d%m%Y"),
            'type': 'ir.actions.act_window',
            'res_model': 'vocab.test.daily',
            'view_mode': 'tree',
            'domain': [('id', 'in', daily_ids.ids)],
            'context': {'create': False, 'delete': False},
            'target': 'current',
        }
        return action

    def action_open_test_daily(self):
        pass

