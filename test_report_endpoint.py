import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from partners.models import Partner
from parcels.models import Parcel
from production.models import HarvestedProduct
from django.db.models import Sum

print("Testing report data generation...")
print("=" * 50)

# Test parcels query
parcels = Parcel.objects.all().select_related('partner')
print(f"\nTotal parcels: {parcels.count()}")

for parcel in parcels[:3]:  # Test first 3
    print(f"\nParcel ID: {parcel.id}")
    print(f"  Code: {getattr(parcel, 'code', f'Parcela-{parcel.id}')}")
    print(f"  Partner: {parcel.partner}")
    print(f"  Partner first_name: {parcel.partner.first_name if parcel.partner else 'None'}")
    print(f"  Partner last_name: {parcel.partner.last_name if parcel.partner else 'None'}")
    print(f"  Surface: {parcel.surface}")
    
    # Test production query
    production = HarvestedProduct.objects.filter(parcel=parcel)
    total_prod = production.aggregate(Sum('quantity'))['quantity__sum'] or 0
    print(f"  Total production: {total_prod}")
    
    # Calculate yield
    surface = float(parcel.surface) if parcel.surface else 0
    yield_per_ha = float(total_prod) / surface if surface > 0 else 0
    print(f"  Yield per ha: {yield_per_ha}")

print("\n" + "=" * 50)
print("Test completed successfully!")
