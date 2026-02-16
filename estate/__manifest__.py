{
    'name': "Real Estate",
    'depends': ['base'],
    'application': True,
    'author': 'Odoo S.A.',
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
}