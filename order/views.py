import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import OrderSerializer, MyOrderSerializer
from .models import Order


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.uuid
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            stripe.api_key = settings.STRIPE_SECRET_KEY
            YOUR_DOMAIN = settings.FRONTEND_URL
            try:
                total = 0
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
                    total += float(product.discounted_price) * count

                checkout_session = stripe.checkout.Session.create(
                    line_items=product_list,
                    mode="payment",
                    success_url=YOUR_DOMAIN + "checkout/success/",
                    cancel_url=YOUR_DOMAIN,
                    customer_email=serializer.validated_data.get("email"),
                    payment_method_types=["card"],
                )

                serializer.save(total=total, checkout_session_id=checkout_session.id)

                return Response(
                    {"id": checkout_session.id}, status=status.HTTP_201_CREATED
                )

            except Exception as e:
                return Response(
                    {"error": {"message": str(e)}},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )


class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyOrderSerializer

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
