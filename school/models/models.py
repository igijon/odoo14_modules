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
    #Se declara como un field pero no se guarda en BDD porque es simplemente una
    #consulta a partir de many2one que sí se guarda en BDD
    students = fields.One2many("school.student", 'classroom')
    teachers = fields.Many2many('school.teacher')

class teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Los profesores'

    name = fields.Char()
    # un profesor puede dar clase en varias aulas y en un aula, varios profesores
    classrooms = fields.Many2many('school.classroom')