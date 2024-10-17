from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product
from django.contrib.auth.decorators import login_required
from django.db.models import Q



@login_required
def home(request):
    products = Product.objects.all()
    product_details = {}
    for product in products:
        # Counting total products for the current product name
        total_count = Product.objects.filter(name=product.name).count()

        # Counting products in office for the current product name
        total_in_office = Product.objects.filter(name=product.name, office_status='in_office').count()

        # Counting products at event for the current product name
        total_at_event = Product.objects.filter(name=product.name, office_status='in_event').count()

        # If the product name is not already in product_details, add it
        if product.name not in product_details:
            product_details[product.name] = {
                'name': product.name,
                'count': total_count,
                'in_office': total_in_office,
                'out_office': total_at_event
            }
    sorted_products = sorted(product_details.values(), key=lambda x: x['count'], reverse=True)
    context = {'products': sorted_products}  # Convert dictionary values to a list
    return render(request, 'home.html', context)

@login_required
def home_location(request):
    if request.method == 'POST':
        warehouse_location = request.POST.get('warehouse_location')
        if warehouse_location=="":
             products = Product.objects.all()
        elif warehouse_location == 'other':
            excluded_locations = ['Mumbai', 'Delhi', 'Bangalore']
            products = Product.objects.exclude(warehouse_location__in=excluded_locations)
        else:
            products = Product.objects.filter(warehouse_location=warehouse_location)

        product_details = {}
        for product in products:
            # Counting total products for the current product name
            total_count = products.filter(name=product.name).count()

            # Counting products in office for the current product name
            total_in_office = products.filter(name=product.name, office_status='in_office').count()

            # Counting products at event for the current product name
            total_at_event = products.filter(name=product.name, office_status='in_event').count()

            # If the product name is not already in product_details, add it
            if product.name not in product_details:
                product_details[product.name] = {
                    'name': product.name,
                    'count': total_count,
                    'in_office': total_in_office,
                    'out_office': total_at_event
                }
        sorted_products = sorted(product_details.values(), key=lambda x: x['count'], reverse=True)
        context = {'products': sorted_products,'warehouse_location':warehouse_location}  # Convert dictionary values to a list
        return render(request, 'home.html', context)
    return redirect('home')


@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        qr_code = request.POST.get('qr_code')
        serial_number = request.POST.get('serial_number')
        model = request.POST.get('model')
        configuration = request.POST.get('configuration')
        working_status = request.POST.get('working_status')
        warehouse_location = request.POST.get('warehouse_location')
        if warehouse_location == 'other':
            warehouse_location=request.POST.get('custom_warehouse_location')
        buy_date = request.POST.get('buy_date')
        brand_name = request.POST.get('brand_name')
        office_status = request.POST.get('office_status')
        if office_status == 'other':
            office_status = request.POST.get('custom_office_status')
        # Check if a product with the given QR code already exists
        existing_product = Product.objects.filter(qr_code=qr_code).first()
        if existing_product:
            # If product with QR code already exists, display error message and pre-fill form
            messages.error(request, 'A product with this QR code already exists.')
            return render(request, 'add_product.html', {'name': name, 'qr_code': qr_code, 'serial_number': serial_number,
                                                        'model': model, 'configuration': configuration,
                                                        'working_status': working_status,
                                                        'warehouse_location': warehouse_location, 'buy_date': buy_date,
                                                        'brand_name': brand_name, 'office_status': office_status})

        # If the product does not exist, create a new Product object
        product = Product(
            name=name,
            qr_code=qr_code,
            serial_number=serial_number,
            model=model,
            configuration=configuration,
            working_status=working_status,
            warehouse_location=warehouse_location,
            buy_date=buy_date,
            brand_name=brand_name,
            office_status=office_status
        )
        product.save()

        messages.success(request, 'Product added successfully.')
        return redirect('add_product')  # Redirect back to the form page to display the success message

    # If request method is not POST, render the form template
    return render(request, 'add_product.html')


# Writing code to see the detials
@login_required
def product_details(request):
    if request.method == 'POST':
        selected_product_name = request.POST.get('product_name')
        products = Product.objects.filter(name=selected_product_name)
        context = {'products': products,'selected_product_name':selected_product_name}
        return render(request, 'product_details.html', context)
    else:
        all_product_names = Product.objects.values_list('name', flat=True).distinct()
        context = {'all_product_names': all_product_names}
        return render(request, 'product_selection.html', context)

@login_required
def product_details_location(request):
    if request.method == 'POST':
        selected_product_name = request.POST.get('product_name')
        selected_warehouse_location = request.POST.get('warehouse_location')
        print(selected_product_name,selected_warehouse_location)
        products = Product.objects.filter(name=selected_product_name, warehouse_location=selected_warehouse_location)
        print(products)
        context = {
            'products': products,
            'selected_product_name': selected_product_name,
            'warehouse_location': selected_warehouse_location
        }
        return render(request, 'product_details.html', context)
    return redirect('home')

@login_required
def qr_code_input(request):
    if request.method == 'POST':
        qr_code = request.POST.get('qr_code')
        qr_code=qr_code.upper()
        try:
            product = Product.objects.get(Q(qr_code=qr_code) | Q(serial_number=qr_code))
            print(product)
            context = {'product': product}
            return render(request, 'qrcode_input.html', context)
        except Product.DoesNotExist:
            message = "Product with the provided QR code or Serial number does not exist."
            return render(request, 'qrcode_input.html', {'message': message})
    else:
        return render(request, 'qrcode_input.html')

import pandas as pd


@login_required
def upload_products(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if file.name.endswith('.xls') or file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
            for index, row in df.iterrows():
                # Create Product object from Excel data
                product_data = {}
                for column in df.columns:
                    # Check if the column exists and if its value is not NaN
                    if column in row and not pd.isna(row[column]):
                        product_data[column] = row[column]
                    else:
                        product_data[column] = " "  # Set to None if value is NaN

                product = Product(**product_data)
                product.save()
            meassage ='File uploaded successfully!'
            return render(request, 'upload_products.html',{'message':meassage})
        else:
            meassage='Invalid file format. Please upload a valid Excel file.'
            return render(request, 'upload_products.html',{'message':meassage})
    return render(request, 'upload_products.html')



# now going for update product
@login_required
def update_product(request):
    if request.method == 'POST':
        qr_code = request.POST.get('qr_code')
        try:
            product = Product.objects.get(qr_code=qr_code)
            context = {'product': product}
            return render(request, 'update_product.html', context)
        except Product.DoesNotExist:
            message = "Product with the provided QR code does not exist."
            return render(request, 'update_product.html', {'message': message})
    else:
        return redirect('home')


@login_required
def update_product_details(request):
    if request.method == 'POST':
        qr_code = request.POST.get('qr_code')
        try:
            product = Product.objects.get(qr_code=qr_code)
            product.name = request.POST.get('name')
            product.serial_number = request.POST.get('serial_number')
            product.model = request.POST.get('model')
            product.configuration = request.POST.get('configuration')
            product.working_status = request.POST.get('working_status')
            # Get the selected warehouse location from the form
            warehouse_location = request.POST.get('warehouse_location')

            if warehouse_location == "other":
                # If 'other' is selected, use the custom warehouse location
                custom_warehouse_location = request.POST.get('custom_warehouse_location')
                product.warehouse_location = custom_warehouse_location
            else:
                # Use the selected predefined warehouse location
                product.warehouse_location = warehouse_location

            product.brand_name = request.POST.get('brand_name')
            office_status = request.POST.get('office_status')
            if office_status== "other":
                product.office_status= request.POST.get('custom_office_status')
            else:
                product.office_status=office_status

            product.save()
            products = Product.objects.filter(name=product.name)
            context = {'products': products,'selected_product_name': product.name}
            return render(request, 'product_details.html', context)
            # return redirect('home')
        except Product.DoesNotExist:
            message = "Product with the provided QR code does not exist."
            return render(request, 'update_product.html', {'message': message})
    else:
        return redirect('home')
