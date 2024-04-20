from odoo import api, fields, models


class VocabTopic(models.Model):
    _name = "vocab.topic"
    _description = "Vocab Topic"

    name = fields.Char()

