import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tenants.models import Organization
from tenants.middleware import set_current_organization
from partners.models import Partner
from parcels.models import Parcel
from production.models import HarvestedProduct
from users.models import User

print("Testing San Juan organization data...")
print("=" * 50)

# Get San Juan organization
try:
    org = Organization.objects.get(subdomain='sanjuan', is_active=True)
    print(f"✓ Organization found: {org.name}")
except Organization.DoesNotExist:
    print("✗ San Juan organization not found!")
    exit(1)

# Set as current organization
set_current_organization(org)

# Check data
partners = Partner.objects.all()
parcels = Parcel.objects.all()
products = HarvestedProduct.objects.all()

print(f"\nData for {org.name}:")
print(f"  Partners: {partners.count()}")
print(f"  Parcels: {parcels.count()}")
print(f"  Harvested Products: {products.count()}")

if parcels.count() > 0:
    print(f"\nSample parcels:")
    for parcel in parcels[:3]:
        print(f"  - {parcel.code}: {parcel.partner.full_name if parcel.partner else 'No partner'}")
        prod = HarvestedProduct.objects.filter(parcel=parcel)
        print(f"    Production: {prod.count()} records")

# Check users with access
print(f"\nUsers with access to {org.name}:")
partners_with_users = Partner.objects.filter(user__isnull=False)
for partner in partners_with_users[:5]:
    print(f"  - {partner.user.username}: {partner.full_name}")

print("\n" + "=" * 50)
