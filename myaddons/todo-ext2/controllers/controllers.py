# -*- coding: utf-8 -*-
from odoo import http

# class Todo-ext2(http.Controller):
#     @http.route('/todo-ext2/todo-ext2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/todo-ext2/todo-ext2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('todo-ext2.listing', {
#             'root': '/todo-ext2/todo-ext2',
#             'objects': http.request.env['todo-ext2.todo-ext2'].search([]),
#         })

#     @http.route('/todo-ext2/todo-ext2/objects/<model("todo-ext2.todo-ext2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('todo-ext2.object', {
#             'object': obj
#         })