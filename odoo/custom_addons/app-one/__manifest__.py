{
    'name': "App One",
    'summary': "A brief description of your module's purpose.",
    'description': "A more detailed description of your module's functionality.",
    'author': "Hussien Ellathy",
    'category': 'Custom',  # Replace with appropriate category if applicable
    'version': '17.0.0.1.0',
    'depends': ['base'],
    'data': [
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}

