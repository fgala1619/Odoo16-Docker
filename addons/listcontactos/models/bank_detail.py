from odoo import api, fields, models


class BankDetails(models.Model):
    _name = 'bank.detail'
    _rec_name = 'bank_id'
    _description = 'New Description'

    bank_id = fields.Many2one("res.bank", string="Bank", required=True)
    card_type = fields.Selection(string="", selection=[('cr', 'Credit'), ('db', 'Debit'), ], required=True, )
    status = fields.Selection(string="Status", selection=[('current', 'Current'), ('expired', 'Expired'), ],
                              required=True, )
    contact_id = fields.Many2one("contactos", string="Contactos")
