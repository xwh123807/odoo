# -*- coding: utf-8 -*-
from odoo import http

# class Todo-all(http.Controller):
#     @http.route('/todo-all/todo-all/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/todo-all/todo-all/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('todo-all.listing', {
#             'root': '/todo-all/todo-all',
#             'objects': http.request.env['todo-all.todo-all'].search([]),
#         })

#     @http.route('/todo-all/todo-all/objects/<model("todo-all.todo-all"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('todo-all.object', {
#             'object': obj
#         })