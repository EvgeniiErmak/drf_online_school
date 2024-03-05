# materials/payment.py
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateProductView(APIView):
    def post(self, request, format=None):
        product = stripe.Product.create(
            name=request.data.get('name')
        )
        return Response(product)


class CreatePriceView(APIView):
    def post(self, request, format=None):
        price = stripe.Price.create(
            currency="usd",
            unit_amount=int(request.data.get('unit_amount')),  # Цена в центах
            recurring={"interval": "month"},
            product_data={"name": request.data.get('product_name')},
        )
        return Response(price)


class CreateCheckoutSession(APIView):
    def post(self, request, *args, **kwargs):
        # Создание цены
        try:
            price = stripe.Price.create(
                currency="usd",
                unit_amount=1000,
                product="your_product_id",
            )
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Создание сессии оплаты
        try:
            session = stripe.checkout.Session.create(
                success_url="https://example.com/success",
                cancel_url="https://example.com/cancel",
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price.id,
                        "quantity": 1,
                    },
                ],
                mode="payment",
            )
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"id": session.id})
