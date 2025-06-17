{
    'name': 'KODE Sports Club Membership',
    'version': '1.0',
    'summary': 'Membership management for KODE Sports Club',
    'description': 'Manages member details, renewals, branches, and access control.',
    'author': 'Abdelrahman Naser',
    'depends': ['base','mail','sale'],
    'data': [
        # Security Files
        'security/groups.xml',
        'security/rules.xml',
        'security/ir.model.access.csv',

        # data
        'data/ir_sequence_data.xml',

        # wizzard
        'wizards/blacklist_wizard_view.xml',
        'wizards/revision_request_wizard_view.xml',

        # Views Files
        'views/menus.xml',
        'views/kode_member_views.xml',
        'views/kode_branch_views.xml',
        'views/res_partner_view.xml',
        'views/blacklist_history_view.xml',
        'views/blacklist_revision_request_view.xml',

        # reports
        'reports/member_report.xml',

    ],
    'installable': True,
    'application': True,
}