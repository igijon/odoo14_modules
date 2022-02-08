# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student(models.Model):
    _name = 'school.student'
    _description = 'school.student'
    
    #Indicamos cómo aparece en la vista que no es de sólo lectura y que es obligatorio
    # Help nos permite que cuando nos posicionamos con el ratón aparezca el mensaje
    name = fields.Char(string="Nombre", readonly=False, required=True, help='Este es el nombre')
    birth_year = fields.Integer()
    description = fields.Text()
    inscription_date = fields.Date()
    last_login = fields.Datetime()
    is_student = fields.Boolean()
    photo = fields.Image(max_width=200, max_height=200) 
    # Field binario pero específico para imágenes