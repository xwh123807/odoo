# -*- coding: utf-8 -*-
from odoo import http

# class Todo-ext(http.Controller):
#     @http.route('/todo-ext/todo-ext/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/todo-ext/todo-ext/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('todo-ext.listing', {
#             'root': '/todo-ext/todo-ext',
#             'objects': http.request.env['todo-ext.todo-ext'].search([]),
#         })

#     @http.route('/todo-ext/todo-ext/objects/<model("todo-ext.todo-ext"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('todo-ext.object', {
#             'object': obj
#         })