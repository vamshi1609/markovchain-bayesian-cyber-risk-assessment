import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','spatialdata.settings')
django.setup()
from django.urls import reverse
print('admin_cyber_risk', reverse('admin_cyber_risk'))
