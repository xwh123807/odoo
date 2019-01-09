# -*- coding: utf-8 -*-
from odoo import http

# class Hr.evaluation(http.Controller):
#     @http.route('/hr.evaluation/hr.evaluation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr.evaluation/hr.evaluation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr.evaluation.listing', {
#             'root': '/hr.evaluation/hr.evaluation',
#             'objects': http.request.env['hr.evaluation.hr.evaluation'].search([]),
#         })

#     @http.route('/hr.evaluation/hr.evaluation/objects/<model("hr.evaluation.hr.evaluation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr.evaluation.object', {
#             'object': obj
#         })