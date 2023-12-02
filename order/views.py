from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import stripe
from .serializers import OrderSerializer


@api_view(["POST"])
def checkout(request):
    data = request.data
    serializer = OrderSerializer(data=data)

    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY
        YOUR_DOMAIN = settings.FRONTEND_URL
        try:
            total_amount = 0
            product_list = []

            for item in serializer.validated_data.get("products"):
                product = item.get("product")
                count = item.get("count")
                product_details = {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": product.name,
                        },
                        "unit_amount": int(float(product.discounted_price) * 100),
                    },
                    "quantity": count,
                }
                product_list.append(product_details)
                total_amount += float(product.discounted_price) * count

            checkout_session = stripe.checkout.Session.create(
                line_items=product_list,
                mode="payment",
                success_url=YOUR_DOMAIN + "/checkout/success",
                cancel_url=YOUR_DOMAIN,
                customer_email=serializer.validated_data.get("email"),
                payment_method_types=["card"],
            )

            serializer.save(
                total_amount=total_amount, stripe_session_id=checkout_session.id
            )

            return Response({"id": checkout_session.id}, 201)

        except Exception as e:
            return Response({"error": {"message": str(e)}}, 500)

    return Response(serializer.errors, 400)
