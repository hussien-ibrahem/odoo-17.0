{
    'name': "App One",
    'summary': "A brief description of your module's purpose.",
    'description': "A more detailed description of your module's functionality.",
    'author': "Hussien Ellathy",
    'category': 'Custom',  # Replace with appropriate category if applicable
    'version': '17.0.0.1.0',
    'depends': ['base','sale_management','mail' , 'contacts'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/property_history_view.xml',
        'wizard/change_state_wizard_view.xml',
        'reports/property_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'app-one/static/assets/css/property.css'
        ],
    },
    'license': 'LGPL-3',
    'application': True,
}
