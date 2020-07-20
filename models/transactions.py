from odoo import models, fields, api

class Transactions(models.Model):
    _name = 'transactions'
    _rec_name = 'provider_id'
    _description = 'Transactions module'

    station_id = fields.Many2one('charging.station')

    session_id = fields.Char(string='Session ID')
    provider_id = fields.Char(string='Provider ID')
    evse_id = fields.Char(string='EVSE ID')
    partner_product_id = fields.Char(string='Partner Product ID')
    uid = fields.Char(string='UID')
    metering_signature = fields.Integer(string="Metering signature")
    charging_start = fields.Datetime(string='Charging start')
    charging_end = fields.Datetime(string='Charging end')
    session_start = fields.Datetime(string='Session start')
    session_end = fields.Datetime(string='Session end')
    meter_value_start = fields.Float(string='Meter value start')
    meter_value_end = fields.Float(string='Meter value end')
    country_code = fields.Char(string='Country Code')
   