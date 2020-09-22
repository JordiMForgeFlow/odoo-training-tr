# -*- coding: utf-8 -*-
{
    'name': "Open Academy",

    'summary': "Manage Courses",

    'description': """
        Open Academy module for managing course trainings
    """,

    'author': "ForgeFlow",
    'website': "http://www.github.com/JordiMForgeFlow",
    'category': 'Uncategorized',
    'version': '13.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/course_views.xml',
        'views/session_views.xml',
        'views/partner.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
