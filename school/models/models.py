# -*- coding: utf-8 -*-
from odoo import models, fields, api
import secrets
import logging

_logger = logging.getLogger(__name__)

class student(models.Model):
    _name = 'school.student'
    _description = 'school.student'
    
    name = fields.Char(string="Nombre", readonly=False, required=True, help='Este es el nombre')
    birth_year = fields.Integer()
    
    password = fields.Char(compute='_get_password', store=True) 

    description = fields.Text()
    inscription_date = fields.Date()
    last_login = fields.Datetime()
    is_student = fields.Boolean()
    photo = fields.Image(max_width=200, max_height=200) 
    classroom = fields.Many2one("school.classroom", ondelete='set null', help='Clase a la que pertenece')
    teachers = fields.Many2many('school.teacher', related='classroom.teachers', readonly=True)
    
    @api.depends('name') 
    def _get_password(self):
        print(self)
        for student in self:
            student.password = secrets.token_urlsafe(12) 
            _logger.debug('\033[94m'+str(student)+'\033[0m')

class classroom(models.Model):
    _name = 'school.classroom'
    _description = 'Las clases'

    name = fields.Char() 
    students = fields.One2many(string="Alumnos", comodel_name='school.student', inverse_name='classroom')
    
    teachers = fields.Many2many(comodel_name='school.teacher',
                                relation='teachers_classroom',
                                column1='classroom_id',
                                column2='teacher_id')

    teachers_last_year = fields.Many2many(comodel_name='school.teacher',
                                relation='teachers_classroom_ly',
                                column1='classroom_id',
                                column2='teacher_id')
    
    """ Campo computado relacional: aunque no sea común vamos a considerar que una clase tiene un coordinador que 
    será un profesor, y que un profesor puede ser coordinador de muchas clases.
    Para este ejemplo, consideramos que el coordinador va a ser el primero de la lista de profesores
    de la clase. Tenemos que poner el id para que funcione correctamente, porque lo que necesita es el
    identificador de la clave ajena a la que apuntará """
    coordinator = fields.Many2one('school.teacher', compute='_get_coordinator')

    def _get_coordinator(self):
        for classroom in self:
            if len(classroom.teachers) > 0:
                # Si la clase no tiene profesores asociados esto fallará por ahora
                classroom.coordinator = classroom.teachers[0].id


class teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Los profesores'

    name = fields.Char()
    # un profesor puede dar clase en varias aulas y en un aula, varios profesores
    classrooms = fields.Many2many(comodel_name='school.classroom',
                                  relation='teachers_classroom',
                                  column1='teacher_id',
                                  column2='classroom_id')

    # Queremos hacer una referencia a clases del año pasado.
    classrooms_ly = fields.Many2many(comodel_name='school.classroom',
                                  relation='teachers_classroom_ly',
                                  column1='teacher_id',
                                  column2='classroom_id')
