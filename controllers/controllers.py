# -*- coding: utf-8 -*-
from odoo import http

# class Charging(http.Controller):
#     @http.route('/charging/charging/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/charging/charging/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('charging.listing', {
#             'root': '/charging/charging',
#             'objects': http.request.env['charging.charging'].search([]),
#         })

#     @http.route('/charging/charging/objects/<model("charging.charging"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('charging.object', {
#             'object': obj
#         })