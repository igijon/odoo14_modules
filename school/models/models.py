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
    
    # También podemos hacerlo con una función lambda. Estas funciones son funciones que aceptan sólo una línea de código
    # aunque dicha línea de código llame a otra función.
    password = fields.Char(default=lambda p: secrets.token_urlsafe(12)) 
    

    description = fields.Text()

    # También es muy útil establecer como valor por defecto en los campos Date, la fecha de hoy
    inscription_date = fields.Date(default=lambda d: fields.Date.today())

    # Si quiero establecer por defecto la fecha y hora
    last_login = fields.Datetime(default=lambda d: fields.Datetime.now())
    
    is_student = fields.Boolean()
    photo = fields.Image(max_width=200, max_height=200) 
    classroom = fields.Many2one("school.classroom", ondelete='set null', help='Clase a la que pertenece')
    teachers = fields.Many2many('school.teacher', related='classroom.teachers', readonly=True)


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
    
    coordinator = fields.Many2one('school.teacher', compute='_get_coordinator')

    """ Otro campo calculado (sin sentido, sólo ejemplo):  Vamos a mostrar un campo All teachers
    en el que aparezcan todos los profesores, los actuales y los del año pasado"""
    all_teachers = fields.Many2many('school.teacher', compute="_get_teacher")

    def _get_coordinator(self):
        for classroom in self:
            if len(classroom.teachers) > 0:
                # Si la clase no tiene profesores asociados esto fallará por ahora
                classroom.coordinator = classroom.teachers[0].id

    def _get_teacher(self):
        for classroom in self:
            # para trabajar acepta o lista de id o recordset, las dos cosas le valen. 
            # En este caso le metemos recordset
            classroom.all_teachers = classroom.teachers + classroom.teachers_last_year


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
