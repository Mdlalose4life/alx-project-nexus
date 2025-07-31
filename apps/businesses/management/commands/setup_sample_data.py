from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db import transaction
from apps.businesses.models import Business, BusinessCategory
from apps.products.models import Product, ProductCategory
from faker import Faker
import random
import uuid

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Create sample data for development'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--businesses',
            type=int,
            default=10,
            help='Number of businesses to create'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=50,
            help='Number of products to create'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data'
        )
    
    def handle(self, *args, **options):
        if options['clear']:
            self.clear_existing_data()
        
        self.stdout.write('Creating sample data...')
        
        try:
            with transaction.atomic():
                # Create categories
                self.create_categories()
                
                # Create users
                users = self.create_users(options['businesses'])
                
                # Create businesses
                businesses = self.create_businesses(users)
                
                # Create products with unique slugs
                self.create_products(businesses, options['products'])
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created {len(businesses)} businesses '
                        f'and {options["products"]} products'
                    )
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating sample data: {str(e)}')
            )
            raise
    
    def clear_existing_data(self):
        """Clear existing sample data"""
        self.stdout.write('Clearing existing data...')
        
        # Delete in reverse order of dependencies
        Product.objects.all().delete()
        Business.objects.all().delete()
        User.objects.filter(username__startswith='business_owner_').delete()
        
        self.stdout.write('Existing data cleared.')
    
    def create_categories(self):
        """Create business and product categories"""
        business_categories = [
            ('Spaza Shops', 'spaza-shops', 'Local convenience stores'),
            ('Restaurants', 'restaurants', 'Food and dining'),
            ('Electronics', 'electronics', 'Electronic goods and repairs'),
            ('Fashion', 'fashion', 'Clothing and accessories'),
            ('Services', 'services', 'Various local services'),
        ]
        
        for name, slug, desc in business_categories:
            BusinessCategory.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'description': desc}
            )
        
        product_categories = [
            ('Food & Beverages', 'food-beverages'),
            ('Electronics', 'electronics'),
            ('Clothing', 'clothing'),
            ('Home & Garden', 'home-garden'),
            ('Health & Beauty', 'health-beauty'),
        ]
        
        for name, slug in product_categories:
            ProductCategory.objects.get_or_create(
                slug=slug,
                defaults={'name': name}
            )
    
    def create_users(self, count):
        """Create sample users"""
        users = []
        existing_usernames = set(User.objects.filter(
            username__startswith='business_owner_'
        ).values_list('username', flat=True))
        
        for i in range(count):
            username = f'business_owner_{i}'
            # Skip if user already exists
            if username in existing_usernames:
                try:
                    users.append(User.objects.get(username=username))
                    continue
                except User.DoesNotExist:
                    pass
            
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                user_type='business_owner',
                phone_number=f'+2771234567{i:02d}'
            )
            users.append(user)
        return users
    
    def create_businesses(self, users):
        """Create sample businesses"""
        categories = list(BusinessCategory.objects.all())
        businesses = []
        
        # Cape Town coordinates (rough boundaries)
        cape_town_bounds = {
            'lat_min': -34.2,
            'lat_max': -33.7,
            'lon_min': 18.3,
            'lon_max': 18.8
        }
        
        for user in users:
            # Skip if business already exists for this user
            if Business.objects.filter(owner=user).exists():
                businesses.extend(Business.objects.filter(owner=user))
                continue
            
            # Random location in Cape Town area
            lat = random.uniform(
                cape_town_bounds['lat_min'], 
                cape_town_bounds['lat_max']
            )
            lon = random.uniform(
                cape_town_bounds['lon_min'], 
                cape_town_bounds['lon_max']
            )
            
            business = Business.objects.create(
                owner=user,
                name=fake.company(),
                description=fake.text(max_nb_chars=200),
                business_type=random.choice([
                    'spaza_shop', 'restaurant', 'electronics', 
                    'fashion', 'services', 'grocery'
                ]),
                category=random.choice(categories) if categories else None,
                phone_number=f'+2771234567{random.randint(10, 99)}',
                email=fake.email(),
                location=Point(lon, lat),
                address=fake.address(),
                city='Cape Town',
                province='Western Cape',
                postal_code=fake.postcode(),
                is_featured=random.choice([True, False]),
                verification_status='verified'
            )
            businesses.append(business)
        
        return businesses
    
    def create_products(self, businesses, count):
        """Create sample products with unique slugs"""
        categories = list(ProductCategory.objects.all())
        
        # Track used slugs per business to avoid duplicates
        business_slugs = {}
        
        for _ in range(count):
            business = random.choice(businesses)
            category = random.choice(categories) if categories else None
            
            # Generate unique product name and slug
            max_attempts = 10
            for attempt in range(max_attempts):
                product_name = fake.catch_phrase()
                base_slug = slugify(product_name)
                
                # Initialize business slug tracking
                if business.id not in business_slugs:
                    business_slugs[business.id] = set()
                
                # Make slug unique for this business
                slug = base_slug
                counter = 1
                while slug in business_slugs[business.id]:
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                # Check database to be extra sure
                if not Product.objects.filter(business=business, slug=slug).exists():
                    business_slugs[business.id].add(slug)
                    break
                else:
                    # Add UUID to make it absolutely unique
                    slug = f"{base_slug}-{str(uuid.uuid4())[:8]}"
                    business_slugs[business.id].add(slug)
                    break
            
            original_price = random.uniform(10, 1000)
            current_price = original_price * random.uniform(0.7, 1.0)  # Possible discount
            
            try:
                Product.objects.create(
                    business=business,
                    name=product_name,
                    slug=slug,
                    description=fake.text(max_nb_chars=300),
                    category=category,
                    price=round(current_price, 2),
                    original_price=round(original_price, 2) if current_price < original_price else None,
                    stock_quantity=random.randint(0, 100),
                    low_stock_threshold=random.randint(5, 20),
                    is_featured=random.choice([True, False]),
                    status='active'
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f'Failed to create product "{product_name}" for business {business.name}: {str(e)}'
                    )
                )
                continue