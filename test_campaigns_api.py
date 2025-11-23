import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from campaigns.models import Campaign
from campaigns.serializers import CampaignListSerializer

# Obtener campañas
campaigns = Campaign.objects.all()
print(f"Total campañas: {campaigns.count()}")

# Intentar serializar
try:
    serializer = CampaignListSerializer(campaigns, many=True)
    print("Serialización exitosa!")
    print("Datos:", serializer.data)
except Exception as e:
    print(f"Error en serialización: {e}")
    import traceback
    traceback.print_exc()
