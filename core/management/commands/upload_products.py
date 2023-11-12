import csv
import os
import requests
from decimal import Decimal
from io import BytesIO
from PIL import Image
from django.core.management.base import BaseCommand
from django.core.files import File
from product.factories import BrandFactory, CategoryFactory, ProductFactory
from product.models import ProductDetailImage


class Command(BaseCommand):
    help = "Read products data from CSV and push it to the database"

    def _upload_data(self):
        csv_filename = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "..",
                "product",
                "data",
                f"products.csv",
            )
        )
        with open(csv_filename, "r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # Create or get product's brand and category
                brand = BrandFactory.create(name=row["Brand"])
                category = CategoryFactory.create(name=row["Category"])

                # Convert the 'price' string to a Decimal
                price_str = row["Price"]
                price_str = price_str.replace("$", "").replace(",", "")
                price_decimal = Decimal(price_str)

                # Download the image from the URL
                image_url = row["Image"]
                response = requests.get(image_url)

                # Check if the request was successful
                if response.status_code == 200:
                    # Read the image content into a BytesIO buffer
                    image_data = BytesIO(response.content)

                    # Open the image using Pillow (PIL) to ensure it's a valid image
                    try:
                        image = Image.open(image_data)
                    except Exception as e:
                        print(f"Failed to open the image from {image_url}: {e}")
                        continue

                    # Create a File object from the image data
                    image_file = File(image_data, name=os.path.basename(image_url))

                    # Create Product instance
                    product = ProductFactory.create(
                        name=row["Name"],
                        category=category,
                        brand=brand,
                        price=price_decimal,
                        image=image_file,
                    )
                    # Upload additional images for the product detail view
                    detail_image = ProductDetailImage(
                        product=product, image=product.image
                    )
                    detail_image.save()
                else:
                    print(f"Failed to download image from {image_url}")

    def handle(self, *args, **options):
        self._upload_data()
