# -*- coding: utf-8 -*-
from odoo import http

# class Todo-share(http.Controller):
#     @http.route('/todo-share/todo-share/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/todo-share/todo-share/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('todo-share.listing', {
#             'root': '/todo-share/todo-share',
#             'objects': http.request.env['todo-share.todo-share'].search([]),
#         })

#     @http.route('/todo-share/todo-share/objects/<model("todo-share.todo-share"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('todo-share.object', {
#             'object': obj
#         })