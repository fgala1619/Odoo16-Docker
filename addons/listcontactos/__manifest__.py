
{
    'name': 'Contact Management System',
    'version': '1.0.0',
    'summary': 'Management System to keep track of all contact documentation. Features.',
    'description': 'Implement Contact Management System',
    'category': 'General',
    'author': 'Franklin Alvarez Gala',
    'depends': [
        'base',
        'mail'
    ],
    'auto_install': True,
    'data': [
        'security/group_security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/race_view.xml',
        'views/visa_view.xml',
        'views/contacto_view.xml',
        'views/menu_view.xml',
        'report/contact_report.xml'
    ],
    'assets': {
        'web.assets_backend': [
            '/listcontactos/static/src/css/style.css'
        ]
    },
}
