from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Manufacturer, Product, Contract, CreditApplication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


@method_decorator(csrf_exempt, name='dispatch')
class ManufacturerView(View):

    def get(self, request, id=None):
        if id:
            manufacturer = get_object_or_404(Manufacturer, id=id)
            data = {"id": manufacturer.id, "name": manufacturer.name, "created_at": manufacturer.created_at}
        else:
            manufacturers = Manufacturer.objects.all()
            data = [{"id": m.id, "name": m.name, "created_at": m.created_at} for m in manufacturers]
        return JsonResponse(data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        manufacturer = Manufacturer.objects.create(name=data['name'])
        return JsonResponse({"id": manufacturer.id, "name": manufacturer.name, "created_at": manufacturer.created_at})

    def put(self, request, id):
        data = json.loads(request.body)
        manufacturer = get_object_or_404(Manufacturer, id=id)
        manufacturer.name = data['name']
        manufacturer.save()
        return JsonResponse({"id": manufacturer.id, "name": manufacturer.name, "created_at": manufacturer.created_at})

    def delete(self, request, id):
        manufacturer = get_object_or_404(Manufacturer, id=id)
        manufacturer.delete()
        return JsonResponse({"message": "Manufacturer deleted successfully"})

class UniqueManufacturersView(View):
    def get(self, request, contract_id):
        unique_manufacturer_ids = Manufacturer.objects.filter(
            products__credit_applications__contract__id=contract_id
        ).values_list('id', flat=True).distinct()
        return JsonResponse(list(unique_manufacturer_ids), safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class ProductView(View):

    def get(self, request, id=None):
        if id:
            product = get_object_or_404(Product, id=id)
            data = {
                "id": product.id,
                "name": product.name,
                "manufacturer_id": product.manufacturer.id,
                "created_at": product.created_at
            }
        else:
            products = Product.objects.all()
            data = [
                {
                    "id": p.id,
                    "name": p.name,
                    "manufacturer_id": p.manufacturer.id,
                    "created_at": p.created_at
                } for p in products]
        return JsonResponse(data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        manufacturer = get_object_or_404(Manufacturer, id=data['manufacturer_id'])
        product = Product.objects.create(name=data['name'], manufacturer=manufacturer)
        return JsonResponse({
            "id": product.id,
            "name": product.name,
            "manufacturer_id": product.manufacturer.id,
            "created_at": product.created_at
        })

    def put(self, request, id):
        data = json.loads(request.body)
        product = get_object_or_404(Product, id=id)
        manufacturer = get_object_or_404(Manufacturer, id=data['manufacturer_id'])
        product.name = data['name']
        product.manufacturer = manufacturer
        product.save()
        return JsonResponse({
            "id": product.id,
            "name": product.name,
            "manufacturer_id": product.manufacturer.id,
            "created_at": product.created_at
        })

    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)
        product.delete()
        return JsonResponse({"message": "Product deleted successfully"})


@method_decorator(csrf_exempt, name='dispatch')
class ContractView(View):

    def get(self, request, id=None):
        if id:
            contract = get_object_or_404(Contract, id=id)
            data = {"id": contract.id, "contract_number": contract.contract_number, "created_at": contract.created_at}
        else:
            contracts = Contract.objects.all()
            data = [{"id": c.id, "contract_number": c.contract_number, "created_at": c.created_at} for c in contracts]
        return JsonResponse(data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        contract = Contract.objects.create(contract_number=data['contract_number'])
        return JsonResponse({"id": contract.id, "contract_number": contract.contract_number, "created_at": contract.created_at})

    def put(self, request, id):
        data = json.loads(request.body)
        contract = get_object_or_404(Contract, id=id)
        contract.contract_number = data['contract_number']
        contract.save()
        return JsonResponse({"id": contract.id, "contract_number": contract.contract_number, "created_at": contract.created_at})

    def delete(self, request, id):
        contract = get_object_or_404(Contract, id=id)
        contract.delete()
        return JsonResponse({"message": "Contract deleted successfully"})


@method_decorator(csrf_exempt, name='dispatch')
class CreditApplicationView(View):

    def get(self, request, id=None):
        if id:
            credit_application = get_object_or_404(CreditApplication, id=id)
            data = {
                "id": credit_application.id,
                "application_number": credit_application.application_number,
                "contract_id": credit_application.contract.id,
                "products": [p.id for p in credit_application.products.all()],
                "created_at": credit_application.created_at
            }
        else:
            credit_applications = CreditApplication.objects.all()
            data = [
                {
                    "id": c.id,
                    "application_number": c.application_number,
                    "contract_id": c.contract.id,
                    "products": [p.id for p in c.products.all()],
                    "created_at": c.created_at
                } for c in credit_applications]
        return JsonResponse(data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        contract = get_object_or_404(Contract, id=data['contract_id'])
        credit_application = CreditApplication.objects.create(application_number=data['application_number'], contract=contract)
        products = Product.objects.filter(id__in=data['products'])
        credit_application.products.set(products)
        return JsonResponse({
            "id": credit_application.id,
            "application_number": credit_application.application_number,
            "contract_id": credit_application.contract.id,
            "products": [p.id for p in credit_application.products.all()],
            "created_at": credit_application.created_at
        })

    def put(self, request, id):
        data = json.loads(request.body)
        credit_application = get_object_or_404(CreditApplication, id=id)
        contract = get_object_or_404(Contract, id=data['contract_id'])
        credit_application.application_number = data['application_number']
        credit_application.contract = contract
        products = Product.objects.filter(id__in=data['products'])
        credit_application.products.set(products)
        credit_application.save()
        return JsonResponse({
            "id": credit_application.id,
            "application_number": credit_application.application_number,
            "contract_id": credit_application.contract.id,
            "products": [p.id for p in credit_application.products.all()],
            "created_at": credit_application.created_at
        })

    def delete(self, request, id):
        credit_application = get_object_or_404(CreditApplication, id=id)
        credit_application.delete()
        return JsonResponse({"message": "Credit Application deleted successfully"})


