from odoo import models, fields, api

class SupplierPrices(models.Model):
    _name = 'supplier.prices'
    _rec_name = 'identifier'
    _description = 'Supplier prices module'


    station_id = fields.Many2one('charging.station')

    identifier = fields.Char(string='Session ID', help='ID of the supplier price')
    company_name = fields.Char(string='Provider ID')
    evse_id = fields.Char(string='EVSE ID')
    product_id = fields.Char(string='Partner Product ID')
    currency = fields.Char(string='UID')

    # for fees 
    has_minimum_billing_threshold = fields.Boolean(string='Has minimum billing threshold')
    minimum_billing_amount = fields.Float(string='Minimum billing amount')
    has_session_fee = fields.Boolean(string='Has session fee',
                        help="Indicates the session fee")
    session_fee = fields.Float(string='Session fee')
    has_maximum_session_fee = fields.Boolean(string='Has maximum session fee')
    maximum_session_fee = fields.Float(string='Maximum session fee')

    # For time price
    simple_minute_price = fields.Float(string='Simple minute price')
    has_complex_minute_price = fields.Boolean(string='Has complex minute price')
    minimum_duration = fields.Float(string='Minimum duration')
    has_hour_of_the_day = fields.Boolean(string='Has hour of the day')
    interval = fields.Char(string='Interval')
    time_prices = fields.One2many('time.prices','supplier_id', string='Maximum session fee')
    # For kWh price
    has_kWh_price = fields.Boolean(string='Has kWh price')
    kwh_price = fields.Float(string='kWh price')
    minimum_consumed_energy = fields.Float(string='Minimum consumed energy')
    Has_time_based_kwh = fields.Boolean(string='Has time based kwh')
    fee_price = fields.Float(string='fee_price')
    time_price = fields.Float(string='time_price')
    total_kwh_price = fields.Float(string='total kwh price')
    # Total Price 
    total_price = fields.Monetary(  string='Total',
                                    store=True, 
                                    readonly=True, 
                                    compute='_compute_supplier_prices')
      

    # calcule Total Price
    
    @api.one
    @api.depends('minimum_billing_amount', 'session_fee', 'simple_minute_price',
                'time_prices', 'kwh_price', 'minimum_consumed_energy', 'minimum_consumption')
    def _compute_supplier_prices(self):
        """  
        this function is for calcule the total price around multi categorier
        we use all the data from supplier module to get the total price of the 
        charging clients
        """
        self.fee_price = 0
        self.time_price = 0
        self.total_kwh_price = 0
        self.total_price = 0
        # calculate fee price
        if self.session_fee > self.minimum_billing_amount and self.session_fee < self.maximum_session_fee :
            self.fee_price = self.session_fee
        # calculate time price
        if self.has_complex_minute_price:
            if self.interval =="start":
                for line in self.time_prices:
                    timeframe = line.billing_each_timeframe * 60
                    if line.hour_from > line.hour_to:
                        duration = (line.hour_to - line.hour_from) * 60
                    else :
                        duration = (line.hour_to - (24 - line.hour_from)) * 60
                    x = duration % timeframe
                    final_duration = duration + x
                    self.time_price+= final_duration * line.minute_price
            else :
                for line in self.time_prices:
                    timeframe = line.billing_each_timeframe * 60
                    if line.hour_from > line.hour_to:
                        duration = (line.hour_to - line.hour_from) * 60
                    else :
                        duration = (line.hour_to - (24 - line.hour_from)) * 60
                    x = duration % timeframe
                    final_duration = duration - (timeframe - x)
                    self.time_price+= final_duration * line.minute_price
        else : 
            self.time_price = 24 * 60 * self.simple_minute_price     
        # calculate total kwh price
        if self.has_complex_minute_price:
            for line in self.time_prices:
                if line.hour_from > line.hour_to:
                    duration = (line.hour_to - line.hour_from) * 60
                else :
                    duration = (line.hour_to - (24 - line.hour_from)) * 60
                self.total_kwh_price+= duration * line.kwh_price
        
        else : 
            self.total_kwh_price = 24 * self.kwh_price

        # calculate total price
        self.total_price = self.fee_price + self.time_price + self.total_kwh_price
            

class TimePrices(models.Model):
    _name = 'time.prices'
    _rec_name = 'billing_each_timeframe'
    _description = 'Time prices module'

    supplier_id = fields.Many2one('supplier.prices')

    minute_price = fields.Float(string='Minute price')
    billing_each_timeframe = fields.Float(string='Billing each timeframe')
    hour_from = fields.Float(string='Hour from')
    hour_to = fields.Float(string='Hour to')
    kwh_price = fields.Float(string='kWh price')
