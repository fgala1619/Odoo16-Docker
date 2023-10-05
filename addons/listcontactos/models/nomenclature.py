from odoo import api, fields, models


class Race(models.Model):
    _name = 'catalog.race'
    _rec_name = 'name'
    _description = 'New Description'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    state = fields.Selection(string="State", selection=[('draft', 'Draft'), ('review', 'Review'),
                                                        ('completed', 'Completed'), ],
                             default='draft', )

    def name_get(self):
        res = []
        for race in self:
            name = f'{race.name} - {race.description}'
            res.append((race.id, name))
        return res

    def action_change_state_race(self):
        return self.write({'state': self.env.context.get('state')})


class VisaType(models.Model):
    _name = 'catalog.visa_type'
    _rec_name = 'name'
    _description = 'New Visa Type'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    state = fields.Selection(string="State", selection=[('draft', 'Draft'), ('review', 'Review'),
                                                        ('completed', 'Completed'), ],
                             default='draft', )

    def name_get(self):
        res = []
        for visa in self:
            name = f'{visa.name} - {visa.description}'
            res.append((visa.id, name))
        return res

    def action_change_state_visa(self):
        return self.write({'state': self.env.context.get('state')})
