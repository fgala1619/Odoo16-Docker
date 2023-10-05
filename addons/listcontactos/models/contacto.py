from odoo import fields, models, api, _
import re


class Address(models.Model):
    _name = 'contacto.address'
    _rec_name = 'street'
    _description = 'New Address'

    street = fields.Char(string='Street')
    number = fields.Char(string='Number')
    postal_code = fields.Char(string='Postal Code', size=5)
    state_id = fields.Many2one("res.country.state", string='State')
    contact_id = fields.Many2one("contactos", string="Contact")


class Contacto(models.Model):
    _name = 'contactos'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    identity_number = fields.Integer(string="Identity Number", required=True)
    name = fields.Char(string="Name", required=True, tracking=True)
    surnames = fields.Char(string="Surnames", required=True, tracking=True)
    data_entry_date = fields.Date(string="Data Entry Date")
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    age = fields.Integer('Age', compute='_compute_age')
    gender = fields.Selection(selection=[("male", "Male"), ("female", "Female")], string='Gender', default="male",
                              tracking=True)
    race_id = fields.Many2one("catalog.race", string="Race")
    visa_type_id = fields.Many2one("catalog.visa_type", string="Visa Type")
    email = fields.Char(string="Email", required=True, tracking=True)
    bank_ids = fields.One2many("bank.detail", inverse_name="contact_id", string="Bank Details")
    address_ids = fields.One2many("contacto.address", inverse_name="contact_id", string="Address")

    @api.constrains('email')
    def _check_email_format(self):
        for person in self:
            if person.email:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", person.email):
                    raise models.ValidationError('Please enter a valid email address.')

    @api.constrains('postal_code')
    def _check_postal_format(self):
        for person in self:
            if person.postal_code and len(person.postal_code).__ne__(5):
                raise models.ValidationError('Please enter a valid postal code, 5 digits required.')

    @api.depends('date_of_birth')
    def _compute_age(self):
        for person in self:
            person.age = 0
            if person.date_of_birth:
                delta = fields.Date.today() - person.date_of_birth
                person.age = delta.days // 365

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['identity_number'] = self.env['ir.sequence'].next_by_code('identity.seq')
        return super(Contacto, self).create(vals_list)

    # @api.onchange('email')
    # def validate_email(self):
    #     if self.email:
    #         match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
    #         if match is None:
    #             raise ValidationError('Not a valid email address')
