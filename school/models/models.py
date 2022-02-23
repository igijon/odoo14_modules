# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import secrets
import logging
import re

_logger = logging.getLogger(__name__)

class student(models.Model):
    _name = 'school.student'
    _description = 'school.student'
    
    #Indicamos cómo aparece en la vista que no es de sólo lectura y que es obligatorio
    # Help nos permite que cuando nos posicionamos con el ratón aparezca el mensaje
    name = fields.Char(string="Nombre", readonly=False, required=True, help='Este es el nombre')
    birth_year = fields.Integer()

    dni = fields.Char(string="DNI")

    password = fields.Char(default=lambda p: secrets.token_urlsafe(12))

    description = fields.Text()

    inscription_date = fields.Date(default=lambda d: fields.Date.today())
    
    last_login = fields.Datetime(default=lambda d: fields.Datetime.now())

    is_student = fields.Boolean()

    level = fields.Selection([('1','1'),('2','2')])

    photo = fields.Image()
    # Este es el formato tradicional para guardar fotos, aunque ahora hay uno
    # imagen en las versiones actuales de Odoo que veremos después
    classroom = fields.Many2one('school.classroom', domain="[('level','=',level)]", ondelete='set null', help='Clase a la que pertecene')
    teachers = fields.Many2many('school.teacher', related='classroom.teachers', readonly=True)     

    state = fields.Selection([('1','Matriculado'),('2','Estudiante'),('3','Ex-estudiante')], default="1")
   
    @api.constrains('dni')
    def _check_dni(self):
        regex = re.compile('[0-9]{8}[a-z]\Z', re.I)
        for student in self:
            if regex.match(student.dni):
                _logger.info('DNI correcto')
            else:
                raise ValidationError('Formato incorrecto: DNI')

    _sql_constraints = [('dni_uniq', 'unique(dni)', 'DNI can\'t be repeated')]

    def regenerate_password(self):
        for student in self:
            pw = secrets.token_urlsafe(12)
            student.write({'password':pw})

class classroom(models.Model):
    _name = 'school.classroom'
    _description = 'Las clases'
    
    name = fields.Char()
    level = fields.Selection([('1','1'),('2','2')])
    students = fields.One2many(string="Alumnos", comodel_name='school.student', inverse_name='classroom')
    teachers = fields.Many2many(comodel_name='school.teacher', relation='teachers_classroom', column1='classroom_id', column2='teacher_id')
    teachers_last_year = fields.Many2many(comodel_name='school.teacher', relation='teachers_classroom_ly', column1='classroom_id', column2='teacher_id')

    coordinator = fields.Many2one('school.teacher', compute='_get_coordinator')
    all_teachers = fields.Many2many('school.teacher', compute='_get_allteachers')

    def _get_coordinator(self):
        for classroom in self:
            if len(classroom.teachers) > 0:
                classroom.coordinator = classroom.teachers[0].id
            else:
                classroom.coordinator = None

    def _get_allteachers(self):
        for classroom in self:
            classroom.all_teachers = classroom.teachers + classroom.teachers_last_year
            

class teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Los profesores'
    
    name = fields.Char()
    topic = fields.Char()
    phone = fields.Char()

    classrooms = fields.Many2many(comodel_name='school.classroom', relation='teachers_classroom', column1='teacher_id', column2='classroom_id')
    classrooms_last_year = fields.Many2many(comodel_name='school.classroom', relation='teachers_classroom_ly', column1='teacher_id', column2='classroom_id')
