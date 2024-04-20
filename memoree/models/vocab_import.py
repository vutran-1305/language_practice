from odoo import api, fields, models


class VocabImport(models.Model):
    _name = "vocab.import"
    _description = "Vocab Import"

    name = fields.Char()
    value = fields.Char()
    topic_id = fields.Many2one('vocab.topic')
    is_hard = fields.Boolean()

