from odoo import fields, models, api
import re


class Address(models.Model):
    _name = 'contacto.address'
    _rec_name = 'street'
    _description = 'New Address'

    street = fields.Char(string='Street')
    number = fields.Char(string='Number')
    postal_code = fields.Char(string='Postal Code', size=5, required=True)
    state_id = fields.Many2one("res.country.state", string='State')
    contact_id = fields.Many2one("contactos", string="Contact")

    @api.constrains('postal_code')
    def _validar_postal_code(self):
        for digit in self:
            if digit.postal_code and (not digit.postal_code.isdigit() or len(digit.postal_code) != 5):
                raise models.ValidationError('El campo Postal Code debe contener solo dígitos y tener una longitud de 5 caracteres')


class Contacto(models.Model):
    _name = 'contactos'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    identity_number = fields.Char(string="Identity Number", size=5, required=True)
    name = fields.Char(string="Name", required=True, tracking=True)
    surnames = fields.Char(string="Surnames", required=True, tracking=True)
    data_entry_date = fields.Date(string="Data Entry Date")
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    age = fields.Integer('Age', compute='_compute_age')
    gender = fields.Selection(selection=[("male", "Male"), ("female", "Female")], string='Gender', default="male",
                              tracking=True, required=True)
    race_id = fields.Many2one("catalog.race", string="Race")
    visa_type_id = fields.Many2one("catalog.visa_type", string="Visa Type")
    email = fields.Char(string="Email", required=True, tracking=True)
    bank_ids = fields.Many2many("bank.detail", relation='contact_bank_rel', column1='contact_id', column2='bank_id',
                                string="Bank Details")
    address_ids = fields.One2many("contacto.address", inverse_name="contact_id", string="Address")
    state = fields.Selection(string="State", selection=[('draft', 'Draft'), ('review', 'Review'),
                                                        ('completed', 'Completed'), ],
                             default='draft', )

    @api.constrains('email')
    def _check_email_format(self):
        for person in self:
            if person.email:
                # if not re.match(r"[^@]+@[^@]+\.[^@]+", person.email):
                if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", person.email):
                    raise models.ValidationError('Please enter a valid email address.')

    @api.constrains('identity_number')
    def _validar_identity_number(self):
        for contact in self:
            if contact.identity_number and (not contact.identity_number.isdigit() or len(contact.identity_number) != 5):
                raise models.ValidationError('El campo Identity Number debe contener solo dígitos y tener una longitud de 5 caracteres')
            if int(contact.identity_number).__lt__(10000):
                raise models.ValidationError('El campo Identity Number tiene que ser mayor o igual que 10000.')

    @api.constrains('date_of_birth')
    def _validar_date_of_birth(self):
        for contact in self:
            if contact.date_of_birth > fields.Date.today():
                raise models.ValidationError(
                    'La fecha de nacimiento no debe ser mayor a la fecha actual')

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

    def action_change_state_contact(self):
        return self.write({'state': self.env.context.get('state')})

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         vals['identity_number'] = self.env['ir.sequence'].next_by_code('identity.seq')
    #     return super(Contacto, self).create(vals_list)

    # @api.onchange('email')
    # def validate_email(self):
    #     if self.email:
    #         match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
    #         if match is None:
    #             raise ValidationError('Not a valid email address')
