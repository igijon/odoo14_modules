# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student(models.Model):
    _name = 'school.student'
    _description = 'school.student'
    
    name = fields.Char(string="Nombre", readonly=False, required=True, help='Este es el nombre')
    birth_year = fields.Integer()
    
    """ Vamos a crear un campo passwd que sea calculado. Un campo computado es un field normal calculado sobre la marcha """
    password = fields.Char(compute='_get_password')

    description = fields.Text()
    inscription_date = fields.Date()
    last_login = fields.Datetime()
    is_student = fields.Boolean()
    photo = fields.Image(max_width=200, max_height=200) 
    classroom = fields.Many2one("school.classroom", ondelete='set null', help='Clase a la que pertenece')
    teachers = fields.Many2many('school.teacher', related='classroom.teachers', readonly=True)
    
    """ Al método le puede llegar una lista de uno o más estudiantes. Self es una lista de estudiantes, si sólo es uno, tendrá sólo un elemento
    A la función le ponemos el _ para indicar que sea privada
    Si quisiésemos que en lugar de una lista, recibiese un único estudiante, tendríamos que poner un decorador @api.one"""
    def _get_password(self):
        # Podemos imprimir lo que está ocurriendo en el terminal por el momento, después usaremos el log
        print(self)
        # Todas las funciones que calculan campos deben recorrer la lista de estudiantes.
        for student in self:
            # Student es una instancia del modelo student
            student.password = '1234' # Como ejemplo estamos asignando a todos los estudiantes la misma contraseña
            print(student)



class classroom(models.Model):
    _name = 'school.classroom'
    _description = 'Las clases'

    name = fields.Char() # Todos los modelos deben tener un field name
    #Se declara como un field pero no se guarda en BDD porque es simplemente una
    #consulta a partir de many2one que sí se guarda en BDD
    students = fields.One2many(string="Alumnos", comodel_name='school.student', inverse_name='classroom')
    
    #relation: nombre de la tabla intermedia que se genera. Si no, Odoo establece 1.
    #column1 y column2, nombre de las columnas que van a hacer referencia al modelo de la clase actual y de la clase con la que referenciamos
    teachers = fields.Many2many(comodel_name='school.teacher',
                                relation='teachers_classroom',
                                column1='classroom_id',
                                column2='teacher_id')

    #Queremos hacer una referencia a profesores del año pasado
    teachers_last_year = fields.Many2many(comodel_name='school.teacher',
                                relation='teachers_classroom_ly',
                                column1='classroom_id',
                                column2='teacher_id')
    

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
