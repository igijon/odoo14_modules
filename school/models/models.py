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
    classroom = fields.Many2one("school.classroom", ondelete='set null', help='Clase a la que pertenece')
    # ondelete: con set null el estudiante  se queda sin la clase, es la opción por defecto. Con restrict, no se elimina la clase en el estudiante
    
    """ Queremos que el estudiante muestre la lista de profesores que le dan clase, a nivel de BDD no tiene sentido, pero puede tener sentido mostrar la información
        en el modelo.
        En este caso no quiero que la relación sea una nueva tabla, quiero que tire de la intermedia creada entre classroom y teachers y voy a utilizar el atributo
        related. Es importante que el campo destino de related sea igual que el campo al que estamos estableciendo la relación, es decir, classroom.teachers hace
        referencia al atributo teachers de la clase classroom y esta ya tira de la tabla correspondiente.
        
        Si añadimos el atributo store=True, se almacenaría en BDD pero sería información redundante"""
    teachers = fields.Many2many('school.teacher', related='classroom.teachers', readonly=True)
    

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
