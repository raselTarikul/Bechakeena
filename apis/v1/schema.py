import coreapi
from rest_framework.schemas import ManualSchema, AutoSchema

device_registration_schema = ManualSchema(
    description='Register Device',
    fields=[
        coreapi.Field('username', required=True, location='form', type='string', description='username'),
        coreapi.Field('shop_name', required=True, location='form', type='string', description='shop name'),
        coreapi.Field('address', required=True, location='form', type='string', description='address'),
        coreapi.Field('pin', required=True, location='form', type='string', description='pin')
    ]
)

device_login_schema = ManualSchema(
    description='Login Device',
    fields=[
        coreapi.Field('username', required=True, location='form', type='string', description='username'),
        coreapi.Field('pin', required=True, location='form', type='string', description='pin')
    ]
)


device_change_pass_schema = ManualSchema(
    description='Change Password',
    fields=[
        coreapi.Field('username', required=True, location='form', type='string', description='username'),
        coreapi.Field('pin', required=True, location='form', type='string', description='pin'),
        coreapi.Field('new_pin', required=True, location='form', type='string', description='new pin')
    ]
)


create_order_schema = ManualSchema(
    description='Create Order [must provide as array]',
    fields=[
        coreapi.Field('product_id', required=True, location='form', type='integer', description='Product Id'),
        coreapi.Field('quantity', required=True, location='form', description='Quantity'),
    ],

)