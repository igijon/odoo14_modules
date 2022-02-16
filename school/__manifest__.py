# -*- coding: utf-8 -*-
{
    'name': "school",

    'summary': "Módulo para aprender a desarrollar módulos para Odoo 14 utilizando el framework de Odoo y Python",

    'description': "En este módulo crearemos modelos, relaciones entre modelos, vistas, campos enumerados y todo lo más destacado para tener una idea general de la creación de módulos para Odoo",

    'author': 'Inma Gijón',
    'website': 'https://github.com/igijon',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Educación',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml', # Para que se carguen los datos de demo debe estar el fichero aquí
        'demo/students.xml',
    ],
}
