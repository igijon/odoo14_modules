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
    # Field binario pero específico para imágenes
    photo = fields.Image(max_width=200, max_height=200) 
    # Clave ajena a la clave primaria de classroom
    classroom = fields.Many2one("school.classroom")
    
class classroom(models.Model):
    _name = 'school.classroom'
    _description = 'Las clases'

    name = fields.Char() # Todos los modelos deben tener un field name