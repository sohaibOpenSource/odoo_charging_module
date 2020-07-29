# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError
import json
import requests
import base64
from requests.auth import HTTPBasicAuth
import logging
from datetime import datetime

class ChargingStation(models.Model):
    _name = 'charging.station'
    _rec_name = 'name'
    _description = 'Charging station module'

    name = fields.Char(string="Name", required=True, )
    transactions_ids = fields.One2many('transactions', "station_id")


    def get_supplier_prices_data(self):
        """  
        this function is for get data from external api and create record in the 
        transactions module withe the cleaning the data meaning and type
        all the data will be a part of the ERP system just with one click
        """
        try:
            res = requests.get('https://hgy780tcj2.execute-api.eu-central-1.amazonaws.com/dev/data')
            logging.info('https://hgy780tcj2.execute-api.eu-central-1.amazonaws.com/dev/data')
            data = json.loads(res.content.decode('utf-8'))
            logging.info(data)
            for record in data['supplier_prices']:
                
                logging.error(record)
                time = 'time_price'
                minute = 'simple minute price'
                if time in record:
                    for i in range(len(record['time_price'])):
                        record['time_price'][i] = (0, 0, record['time_price'][i]) 
                    min_duration = record['min_duration'].replace(",", ".")
                    kwh = record['kwh Price'].replace(",", ".")
                    cosumed = record['min cosumed energy'].replace(",", ".")
                    max_session = record['max_session fee'].replace(",", ".")
                    billing = record['min billing amount'].replace(",", ".")
                    session = record['session Fee'].replace(",", ".")
                    self.env['supplier.prices'].create({
                                                        'identifier': record['Identifier'],
                                                        'company_name': record['Company name'],
                                                        'evse_id': record['EVSE ID'],
                                                        'product_id': record['Product ID'],
                                                        'currency': record['Currency'][0],
                                                        'has_complex_minute_price': record['has complex minute price'],
                                                        'has_hour_of_the_day': record['has hour day'],
                                                        'minimum_duration': min_duration,
                                                        'interval': record['interval'],
                                                        'has_kWh_price': record['has kwh price'],
                                                        'kwh_price': kwh,
                                                        'minimum_consumed_energy': cosumed,
                                                        'has_maximum_session_fee': record['has max session Fee'],
                                                        'has_minimum_billing_threshold': record['has minimum billing threshold'],
                                                        'has_session_fee': record['has session fee'],
                                                        'maximum_session_fee': max_session,
                                                        'minimum_billing_amount': billing,
                                                        'session_fee': session,
                                                         })
                    logging.error(_(record))
                elif minute in record:
                    min_duration = record['min_duration'].replace(",", ".")
                    max_session = record['max_session fee'].replace(",", ".")
                    billing = record['min billing amount'].replace(",", ".")
                    session = record['session Fee'].replace(",", ".")
                    simple = record['simple minute price'].replace(",", ".")
                    self.env['supplier.prices'].create({
                                                        'identifier': record['Identifier'],
                                                        'company_name': record['Company name'],
                                                        'evse_id': record['EVSE ID'],
                                                        'product_id': record['Product ID'],
                                                        'currency': record['Currency'][0],
                                                        'has_complex_minute_price': record['has complex minute price'],
                                                        'has_maximum_session_fee': record['has max session Fee'],
                                                        'has_minimum_billing_threshold': record['has minimum billing threshold'],
                                                        'has_session_fee': record['has session fee'],
                                                        'minimum_billing_amount': billing,
                                                        'maximum_session_fee': max_session,
                                                        'minimum_duration': min_duration,
                                                        'session_fee': session,
                                                        'simple_minute_price': simple,
                                                                })
                    logging.error(_(record))
                    
                else :
                    kwh = record['kwh Price'].replace(",", ".")
                    cosumed = record['min cosumed energy'].replace(",", ".")
                    max_session = record['max_session fee'].replace(",", ".")
                    billing = record['min billing amount'].replace(",", ".")
                    session = record['session Fee'].replace(",", ".")
                    self.env['supplier.prices'].create({
                                                        'identifier': record['Identifier'],
                                                        'company_name': record['Company name'],
                                                        'evse_id': record['EVSE ID'],
                                                        'product_id': record['Product ID'],
                                                        'currency': record['Currency'][0],
                                                        'has_kWh_price': record['has kwh price'],
                                                        'kwh_price': kwh,
                                                        'minimum_consumed_energy': cosumed,
                                                        'maximum_session_fee': max_session,
                                                        'has_maximum_session_fee': record['has max session Fee'],
                                                        'has_minimum_billing_threshold': record['has minimum billing threshold'],
                                                        'has_session_fee': record['has session fee'],
                                                        'minimum_billing_amount': billing,
                                                        'session_fee': session,
                                                                })
                    logging.error(_(record))
                    
        except:
            raise ValidationError(_('connection is down'))

    def get_data(self):
        """  
        this function is for get data from external api and create record in the 
        transactions module withe the cleaning the data meaning and type
        all the data will be a part of the ERP system just with one click
        """
        try:
            res = requests.get('https://hgy780tcj2.execute-api.eu-central-1.amazonaws.com/dev/data')
            logging.info('https://hgy780tcj2.execute-api.eu-central-1.amazonaws.com/dev/data')
            data = json.loads(res.content.decode('utf-8'))
            logging.info(data)
            for record in data['transactions']:
                logging.error(record)
                value_start = record['Meter value start'].replace(",", ".")
                value_end = record['Meter value end'].replace(",", ".")
                self.env['transactions'].create({
                                                    'session_id': record['Session ID'],
                                                    'provider_id': record['Proveider ID'],
                                                    'evse_id': record['EVSEID'],
                                                    'partner_product_id': record['Partner product ID'],
                                                    'uid': record['UID'],
                                                    'metering_signature': record['Metering signature'],
                                                    'charging_start': record['Charging start'],
                                                    'charging_end': record['Charging end'],
                                                    'session_start': record['Session start'],
                                                    'session_end': record['Session end'],
                                                    'meter_value_start': value_start,
                                                    'meter_value_end': value_end,
                                                    'country_code': record['CountryCode'],
                                                            })
                logging.error(_(record))
        except:
            raise ValidationError(_('connection is down'))

