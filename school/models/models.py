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
    
    name = fields.Char(string="Nombre", readonly=False, required=True, help='Este es el nombre')
    birth_year = fields.Integer()

    """Vamos a añadir un DNI que va a ser de tipo Char. Los DNI tienen que cumplir un patrón
    Para ello, vamos a crear una función con el decorador @api.constrains('dni') y debemos tener en cuenta que este tipo de funciones reciben una lista de estudiantes, no un único estudiante.
    Para hacer este tipo de checkeos vamos a utilizar las expresiones regulares en python"""
    dni = fields.Char(string="DNI")
    
    # También podemos hacerlo con una función lambda. Estas funciones son funciones que aceptan sólo una línea de código
    # aunque dicha línea de código llame a otra función.
    password = fields.Char(default=lambda p: secrets.token_urlsafe(12)) 
    

    description = fields.Text()

    # También es muy útil establecer como valor por defecto en los campos Date, la fecha de hoy
    inscription_date = fields.Date(default=lambda d: fields.Date.today())

    # Si quiero establecer por defecto la fecha y hora
    last_login = fields.Datetime(default=lambda d: fields.Datetime.now())

    # Debemos hacerlo con una función lambda o con un puntero a función como hemos hecho antes con _get_password porque si directamente pusiésemos default: fields.Datetime().now(), se cargaría al iniciar
    # el servicio pero no se cargaría cada vez que se crea un alumno, por ejemplo.
    is_student = fields.Boolean()

    level = fields.Selection([('1','1'),('2','2')])

    photo = fields.Image(max_width=200, max_height=200) 

    """ Para que un estudiante cuando esté relacionado con la clase no pueda tener un level diferente
    al de su clase establecemos un filtro. En este caso recibe una lista de tuplas, cada tupla tiene tres
    elementos, el primer campo se refiere al level remoto (la clase relacionada) y el segundo level al actual
    El actual (no remoto) va sin comilla
    """
    classroom = fields.Many2one("school.classroom", domain="[('level','=',level)]", ondelete='set null', help='Clase a la que pertenece')
    teachers = fields.Many2many('school.teacher', related='classroom.teachers', readonly=True)

    state = fields.Selection([('1', 'Matriculado'), ('2', 'Estudiante'), ('3', 'Ex-estudiante')], default="1")
    
    """Este chequeo también impedirá que estudiantes que no tienen DNI válidos tampoco se puedan crear desde una función. Va a chequear el campo antes de guardarlo SIEMPRE
    Por otro lado, el DNI tiene que ser único. Podemos hacerlo desde Python haciendo la búsqueda para ver si ya existe, pero también se puede establecer la unicidad desde BDD
    El modelo, tiene una variable privada _sql_constraints que por defecto es un array vacío. Permite en cada posición recibir una tupla. El primer valor, será el nombre de la constraint,
    el segundo valor será la restricción en postgresql y por último el mensaje"""
    @api.constrains('dni')
    def _check_dni(self):
        regex = re.compile('[0-9]{8}[a-z]\Z', re.I) #re.I ignoreCase
        for student in self:
            # Ahora vamos a validar si se cumple la condición
            if regex.match(student.dni):
                _logger.info('DNI correcto')
            else:
                # No coinciden por lo que tenemos que informar e impedir que se guarde
                raise ValidationError('Formato incorrecto: DNI')
                # Si el DNI no es válido no nos permitirá guardar

    _sql_constraints = [('dni_uniq', 'unique(dni)', 'DNI can\'t be repeated')] #Todos los mensajes los deberíamos poner en inglés y luego traducir

    #También recibe un recordset
    def regenerate_password(self):
        for student in self:
                pw = secrets.token_urlsafe(12)
                student.write({'password':pw})


class classroom(models.Model):
    _name = 'school.classroom'
    _description = 'Las clases'

    name = fields.Char() 
    level = fields.Selection([('1','1'),('2','2')])
    """Añadimos el campo level que será un desplegable para elegir una opción que se guarda en la BDD
    Recibe una lista de tuplas, el primer valor de la tupla es lo que se guarda en la BDD y el segundo
    el texto que muestra"""
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
            else:
                classroom.coordinator = None # Para que no de error al calcular el coordinador

    def _get_teacher(self):
        for classroom in self:
            # para trabajar acepta o lista de id o recordset, las dos cosas le valen. 
            # En este caso le metemos recordset
            classroom.all_teachers = classroom.teachers + classroom.teachers_last_year


class teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Los profesores'

    name = fields.Char()
    topic = fields.Char()
    phone = fields.Char()

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

class seminar(models.Model):
    _name = 'school.seminar'

    name = fields.Char()
    date = fields.Datetime()
    finish = fields.Datetime()
    hours = fields.Integer()
    classroom = fields.Many2one('school.classroom')