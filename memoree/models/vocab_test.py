from odoo import api, fields, models
from datetime import datetime, date
from ast import literal_eval

class VocabTest(models.Model):
    _name = "vocab.test"
    _description = "Vocab Test"

    name = fields.Char(required=1)
    model_name = fields.Char(string='Model Name', default='vocab.import', store=True)
    domain = fields.Char(string="Filter",  readonly=False, store=True)
    start_time = fields.Date()
    end_time = fields.Date()
    is_limit = fields.Boolean()
    count_word = fields.Integer()
    vocab_test_daily_ids = fields.One2many('vocab.test.daily', 'vocab_test_id', domain=lambda self: [('create_uid', 'in', [self.env.user.id])])
    count_test_daily = fields.Integer()
    check_type = fields.Selection([('totally_same', 'Totally same'), ('have_similarity', 'Have Similarity')], default='totally_same', required=1)
    maximum_similarity_ratio = fields.Float(default=80)

    def action_start_test(self):
        record_domain = []
        if self.domain:
            record_domain = literal_eval(self.domain or "[]")
        record_domain.append(('create_uid', '=', self.create_uid.id))
        vocab_import = self.env['vocab.import'].sudo().search(record_domain)
        if vocab_import:
            if not self.vocab_test_daily_ids:
                values = []
                for vocab in vocab_import:
                    values.append({'vocab_import_id': vocab.id, 'date': date.today(), 'vocab_test_id': self.id})
                daily_ids = self.env['vocab.test.daily'].sudo().create(values)
            else:
                vocab_import_ids = self.vocab_test_daily_ids.mapped("vocab_import_id")
                if vocab_import_ids:
                    values = []
                    for vocab in vocab_import:
                        if vocab not in vocab_import_ids:
                            values.append({'vocab_import_id': vocab.id, 'date': date.today(), 'vocab_test_id': self.id})
                    if values:
                        self.env['vocab.test.daily'].sudo().create(values)

        action = {
            'name': 'Test Daily - %s' % date.today().strftime("%d%m%Y"),
            'type': 'ir.actions.act_window',
            'res_model': 'vocab.test.daily',
            'view_mode': 'tree',
            'domain': [('id', 'in', self.vocab_test_daily_ids.ids)],
            'context': {'create': False, 'delete': False, 'is_hidden_simular_ratio': False},
            'target': 'current',
        }
        if self.check_type != 'have_similarity':
            action['context']['is_hidden_simular_ratio'] = True
        return action

    def action_open_test_daily(self):
        pass

