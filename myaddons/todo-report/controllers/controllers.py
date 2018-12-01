# -*- coding: utf-8 -*-
from odoo import http

# class Todo-report(http.Controller):
#     @http.route('/todo-report/todo-report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/todo-report/todo-report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('todo-report.listing', {
#             'root': '/todo-report/todo-report',
#             'objects': http.request.env['todo-report.todo-report'].search([]),
#         })

#     @http.route('/todo-report/todo-report/objects/<model("todo-report.todo-report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('todo-report.object', {
#             'object': obj
#         })