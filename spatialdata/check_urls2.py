import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','spatialdata.settings')
django.setup()
from django.urls import reverse, get_resolver
print('all names:', sorted(name for name in get_resolver().reverse_dict.keys()))
try:
    print('admin_cyber_risk ->', reverse('admin_cyber_risk'))
except Exception as e:
    print('reverse error', e)
