{
    'name': "To Do App",
    'summary': "Task 1.",
    'description': "This Task is required from the course 10-10-2024",
    'author': "Hussien Ellathy",
    'category': 'Custom',  # Replace with appropriate category if applicable
    'version': '17.0.0.1.0',
    'depends': ['base', 'mail'],
    'data': [
        'views/base_menu.xml',
        'views/task_view.xml',
        'views/employee_view.xml',
        'security/ir.model.access.csv',
        'reports/task_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'to-do-app/static/assets/css/task.css'
        ],
    },
    'license': 'LGPL-3',
    'application': True,
}
