from odoo import api, fields, models


class Race(models.Model):
    _name = 'catalog.race'
    _rec_name = 'name'
    _description = 'New Description'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")

    def name_get(self):
        res = []
        for race in self:
            name = f'{race.name} - {race.description}'
            res.append((race.id, name))
        return res


class VisaType(models.Model):
    _name = 'catalog.visa_type'
    _rec_name = 'name'
    _description = 'New Visa Type'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")


    def name_get(self):
        res = []
        for visa in self:
            name = f'{visa.name} - {visa.description}'
            res.append((visa.id, name))
        return res


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    race_id = fields.Many2one(comodel_name="catalog.race", string="Race", required=False, )
