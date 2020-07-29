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
            true = True
            false = False
            res = requests.get('https://hgy780tcj2.execute-api.eu-central-1.amazonaws.com/dev/data')
            logging.info('https://hgy780tcj2.execute-api.eu-central-1.amazonaws.com/dev/data')
            data = json.loads(res.content.decode('utf-8'))
            logging.info(data)
            for record in data['supplier_prices']:
                logging.error(record)
                minute = 'simple minute price'
                if 'time_price' in record:
                      
                    lines = []
                    for i in range(len(record['time_price'])):
                        if 'billing_each_timeframe' in record['time_price'][i]:    
                            billing_each_timeframe = record['time_price'][i]['billing_each_timeframe']
                        else :
                            billing_each_timeframe = 0
                        if 'hour from' in record['time_price'][i]:    
                            hour_from = record['time_price'][i]['hour from']
                        else :
                            hour_from = 0   
                        if 'hour to' in record['time_price'][i]:    
                            hour_to = record['time_price'][i]['hour to']
                        else :
                            hour_to = 0   
                        if 'minute price' in record['time_price'][i]:    
                            minute_price = record['time_price'][i]['minute price'].replace(",", ".")
                        else :
                            minute_price = 0 
                        if 'kwh price' in record['time_price'][i]:    
                            kwh_price = record['time_price'][i]['kwh price'].replace(",", ".")
                        else :
                            kwh_price = 0              
                        lines.append((0,0,{
                            'billing_each_timeframe': billing_each_timeframe,
                            'hour_from': hour_from,
                            'hour_to': hour_to,
                            'minute_price': minute_price,
                            'kwh_price': kwh_price,
                            }))
                    time_price_lines = lines
                else :
                     time_price_lines = []   
                if 'session Fee' in record:    
                    if record['session Fee'] == 'False':
                        session = record['session Fee'].replace("False", "0")
                    else:
                        session = record['session Fee'].replace(",", ".")
                else :
                    session = 0       
                if 'min_duration' in record:    
                    if record['min_duration'] == 'False':
                        min_duration = record['session Fee'].replace("False", "0")
                    else:
                        min_duration = record['min_duration'].replace(",", ".")
                else :
                    min_duration = 0
                if 'simple minute price' in record:    
                    if record['simple minute price'] == 'False':
                        simple = record['session Fee'].replace("False", "0")
                    else:
                        simple = record['simple minute price'].replace(",", ".")
                else :
                    simple = 0  
                if 'max_session fee' in record:    
                    if record['max_session fee'] == 'False':
                        max_session = record['max_session fee'].replace("False", "0")
                    else:
                        max_session = record['max_session fee'].replace(",", ".")
                else :
                    max_session = 0      
                if 'max_session fee' in record:    
                    if record['min billing amount'] == 'False':
                        billing = record['min billing amount'].replace("False", "0")
                    else:
                        billing = record['min billing amount'].replace(",", ".")
                else :
                    billing = 0  
                if 'min_duration' in record:    
                    if record['min_duration'] == 'False':
                        min_duration = record['min_duration'].replace("False", "0")
                    else:
                        min_duration = record['min_duration'].replace(",", ".")
                else :
                    min_duration = 0  
                if 'interval' in record:    
                    interval = record['interval']   
                else : 
                    interval = ''
                  
                if 'has kwh price' in record:    
                    if record['has kwh price'] == true:
                        has_kwh_price = True
                    else:
                        has_kwh_price = False
                else :
                    has_kwh_price = False    
                if 'kwh Price' in record:    
                    if record['kwh Price'] == 'False':
                        kwh = record['kwh Price'].replace("False", "0")
                    else:
                        kwh = record['kwh Price'].replace(",", ".")
                else :
                    kwh = 0  
                if 'min cosumed energy' in record:    
                    if record['min cosumed energy'] == 'False':
                        cosumed = record['min cosumed energy'].replace("False", "0")
                    else:
                        cosumed = record['min cosumed energy'].replace(",", ".")
                else :
                    cosumed = 0 
                if 'has max session Fee' in record:    
                    if record['has max session Fee'] == true:
                        has_max_session_Fee = True
                    else:
                        has_max_session_Fee = False
                else :
                    has_max_session_Fee = False
                if 'has minimum billing threshold' in record:    
                    if record['has minimum billing threshold'] == true:
                        has_minimum_billing_threshold = True
                    else:
                        has_minimum_billing_threshold = False
                else :
                    has_minimum_billing_threshold = False
                if 'has session fee' in record:    
                    if record['has session fee'] == true:
                        has_session_fee = True
                    else:
                        has_session_fee = False
                else :
                    has_session_fee = False
                if 'has complex minute price' in record:    
                    if record['has complex minute price'] == true:
                        has_complex_minute_price = True
                    else:
                        has_complex_minute_price = False
                else :
                    has_complex_minute_price = False
                if 'has hour day' in record:    
                    if record['has hour day'] == true:
                        has_hour_day = True
                    else:
                        has_hour_day = False
                else :
                    has_hour_day = False
                if 'has complex minute price' in record:    
                    if record['has complex minute price'] == true:
                        has_complex_minute_price = True
                    else:
                        has_complex_minute_price = False
                else :
                    has_complex_minute_price = False                            
                self.env['supplier.prices'].create({
                                                    'identifier': record['Identifier'],
                                                    'company_name': record['Company name'],
                                                    'evse_id': record['EVSE ID'],
                                                    'product_id': record['Product ID'],
                                                    'currency': record['Currency'][0],
                                                    'session_fee': session,
                                                    'minimum_duration': min_duration,
                                                    'simple_minute_price': simple,
                                                    'maximum_session_fee': max_session,
                                                    'minimum_billing_amount': billing,
                                                    'minimum_duration': min_duration,
                                                    'interval': interval,
                                                    'has_kWh_price': has_kwh_price,
                                                    'kwh_price': kwh,
                                                    'minimum_consumed_energy': cosumed,
                                                    'has_maximum_session_fee': has_max_session_Fee,
                                                    'has_minimum_billing_threshold': has_minimum_billing_threshold,
                                                    'has_session_fee': has_session_fee,
                                                    'has_complex_minute_price': has_complex_minute_price,
                                                    'has_hour_of_the_day': has_hour_day,
                                                    'has_complex_minute_price': has_complex_minute_price,
                                                    'time_prices_ids': time_price_lines,
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

