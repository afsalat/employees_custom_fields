from django.urls import path


urlpatterns = [
    path('',)
]

@api_view(['POST'])
def create_product(request):
    try: 
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=404)
        
        variants = request.data.get('variants', [])
        product = serializer.save()
        
        for variant_data in variants:
            variant = Variant.objects.create(product=product, name=variant_data['name'])
            for sub_variant in variant_data['options']:
                SubVariant.objects.create(variant=variant, option=sub_variant, stock=0.00)

        return Response({"message": "successfully added"}, status=200) 
    except Exception as e:
        print(traceback.format_exc())
        return Response({"error": str(e)}, status=500)