import csv
import os
import requests
from decimal import Decimal, InvalidOperation
from io import BytesIO
from PIL import Image
from django.core.management.base import BaseCommand
from django.core.files import File
from product.factories import (
    CategoryFactory,
    ProductFactory,
)
from django.utils.text import slugify


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
                "All Exercise and Fitness.csv",
            )
        )

        with open(csv_filename, "r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # Create or get product's category
                category = CategoryFactory.create(name="Sports and Fitness")

                # Convert the 'price' string to a Decimal
                price = row["actual_price"]
                if price:
                    price_str = price.replace("$", "").replace(",", "").replace("₹", "")
                    try:
                        price_decimal = Decimal(price_str)
                    except InvalidOperation as e:
                        print(f"Failed to convert '{price_str}' to Decimal: {e}")
                        continue
                else:
                    print("Price is empty. Skipping processing for this row.")
                    continue

                # Convert indian rupee to dollar and round
                usd_conversion_rate = Decimal("83")
                price_in_usd = price_decimal / usd_conversion_rate
                price_in_usd_rounded = round(price_in_usd, 0)

                # Download the image from the URL
                image_url = row["image"]
                response = requests.get(image_url)

                # Check if the request was successful
                if response.status_code == 200:
                    # Read the image content into a BytesIO buffer
                    image_data = BytesIO(response.content)

                    # Open the image using Pillow (PIL) to ensure it's a valid image
                    try:
                        Image.open(image_data)
                    except Exception as e:
                        print(f"Failed to open the image from {image_url}: {e}")
                        continue

                    # Create a File object from the image data
                    filename = os.path.basename(image_url)
                    name, extension = os.path.splitext(filename)
                    image_name = slugify(row["name"]) + extension
                    image_file = File(image_data, name=image_name)

                    # Create Product
                    ProductFactory.create(
                        name=row["name"],
                        category=category,
                        price=price_in_usd_rounded,
                        image=image_file,
                    )

                else:
                    print(f"Failed to download image from {image_url}")

    def handle(self, *args, **options):
        self._upload_data()
