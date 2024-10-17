from django.http import HttpResponse
from django.shortcuts import render ,redirect
from django.db.models import Count
from openpyxl import Workbook
from django.db.models import AutoField
from Add_product.models import Product
from .models import EventDetails ,EventProduct ,temporaryaddeventdb
from django.contrib.auth.decorators import login_required
from collections import defaultdict


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import EventDetails


@login_required
def AddeventDetails(request):
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_location = request.POST.get('event_location')
        event_date = request.POST.get('event_date')
        warehouse_location = request.POST.get('warehouse_location')
        person_name = request.POST.get('person_name')
        event_hotel = request.POST.get('event_hotel')  # Retrieve event_hotel from the form

        if person_name == 'other':
            person_name = request.POST.get('custom_person_name')
        
        if EventDetails.objects.filter(event_name=event_name).exists():
            # Display a message or handle the case where the event name already exists
            unique_message = "Event name already exists. Please add some other text with Name." + event_name
            return render(request, 'AddeventDetails.html', {'unique_message': unique_message})

        event_id = EventDetails.objects.count() + 1
        new_event = EventDetails(
            event_name=event_name,
            event_location=event_location,
            event_date=event_date,
            event_id=event_id,
            warehouse_location=warehouse_location,
            person_name=person_name,
            event_hotel=event_hotel  # Save the event_hotel value
        )
        new_event.save()
        return redirect('enter_product_details', event_id=event_id)
    
    return render(request, 'AddeventDetails.html')




# saving the event product detials
@login_required
def enterProductDetails(request, event_id):
    event_details = EventDetails.objects.get(event_id=event_id)
    if request.method == 'POST':
        qr_code = request.POST.get('qr_code')
        event_id = request.POST.get('event_id')
        try:
            if EventProduct.objects.filter(qr_code=qr_code, event_id=event_id).exists():
                message = f"Product with  QR code {qr_code} has already been added. Please scan another product."
                return render(request, 'enter_product_details.html', {'message': message,'event_details': event_details})
            # Fetch event details from EventDetails table
            event_details = EventDetails.objects.get(event_id=event_id)
            Prod = Product.objects.get(qr_code=qr_code)
            if Prod.working_status !="working":
                message=f"Product are not  Working Properly Can you Recheck"
                return render(request, 'enter_product_details.html', {'message': message,'event_details': event_details})
            if Prod.office_status !="in_office":
                message=f"Product with qr code {qr_code} is not in office can you check it ?"
                return render(request, 'enter_product_details.html', {'message': message,'event_details': event_details})
            Prod.office_status="in_event"
            Prod.event_name=event_details.event_name
            Prod.save()
            # Create EventProduct instance and save
            event_product = EventProduct(
                qr_code=qr_code,
                event_id=event_id,
                product_name=Prod.name,
                status=True
            )
            event_product.save()
            message=f'product with {qr_code} is added sucessfully .'
            # Redirect to success page or any other page as needed
            return render(request, 'enter_product_details.html', {'event_details': event_details,'message': message})
        except:
            message="Invalid qr code  can you check your qr code or contact with admin"
            return render(request, 'enter_product_details.html', {'event_details': event_details,'message': message})
    else:
        # Fetch event details based on event_id
        event_details = EventDetails.objects.get(event_id=event_id)
        return render(request, 'enter_product_details.html', {'event_details': event_details})

# Now we have to store

@login_required
def remark_note(request,event_id):
    event_details = EventDetails.objects.get(event_id=event_id)
    if request.method =='POST':
        event_id=request.POST.get('event_id')
        remark_note=request.POST.get('remark_note')
        try:
            event_details = EventDetails.objects.get(event_id=event_id)
            event_details.remark_note=remark_note
            event_details.save()
            return redirect('event_views')
        except:
            message='In valide some Erorr'
            return render(request,'remark_note.html',{'event_details':event_details,'message':message})
    return render(request,'remark_note.html',{'event_details':event_details})


@login_required
def event_selection_view(request):
    if request.method == 'POST':
        selected_event_name = request.POST.get('event')
        try:
            event_details = EventDetails.objects.get(event_name=selected_event_name, status=True)
        except EventDetails.DoesNotExist:
            message = "Currently No Active Event"
            return render(request, 'chalan_views.html', {'message': message})

        event_products = EventProduct.objects.filter(event_id=event_details.event_id, status=True) \
                            .values('product_name') \
                            .annotate(count=Count('product_name'))
        sum_value=event_products.count()
        event_things = EventProduct.objects.filter(event_id=event_details.event_id, status=True)
        product_serial_numbers = defaultdict(list)

        for product in event_things:
            product_info = Product.objects.filter(qr_code=product.qr_code).first()
            if product_info:
                product_serial_numbers[product.product_name].append(product_info.serial_number)
        tempdata =temporaryaddeventdb.objects.filter(event_id=event_details.event_id)

        # Convert defaultdict to list of tuples for easier handling in the template
        product_serial_tuples = list(product_serial_numbers.items())
        product_configurations = {}
        for product in event_products:
            product_info = Product.objects.filter(name=product['product_name']).first()
            if product_info:
                product_configurations[product['product_name']] = product_info.configuration

        context = {
            'event_details': event_details,
            'event_products': event_products,
             'product_configurations': product_configurations,
            'product_serial_tuples': product_serial_tuples,
            'tempdata':tempdata,
            'blank_rows': '00',
            'sum_value':sum_value,
        }

        return render(request, 'chalan.html', context)

    events = EventDetails.objects.filter(status=True).values_list('event_name', flat=True)
    context = {'events': events}
    return render(request, 'chalan_views.html', context)


@login_required
def temporaryaddevent(request, event_id):
    event_details = EventDetails.objects.get(event_id=event_id)
    if request.method == 'POST':
        # Retrieve form data from POST request
        product_name = request.POST.get('product_name')
        count = request.POST.get('count')
        serial_number = request.POST.get('serial_number')
        remark_note = request.POST.get('remark_note', '')
        event_product = temporaryaddeventdb(
            event_id=event_id,
            product_name=product_name,
            count=count,
            serial_number=serial_number,
            remark_note=remark_note
        )
        event_product.save()
        return redirect('temporaryaddevent',event_id=event_id)
    return render(request,'temporaryaddevent.html',{'event_details':event_details})

# event chalan for all
@login_required
def event_selection_all(request):
    if request.method == 'POST':
        selected_event_name = request.POST.get('event')
        try:
            event_details = EventDetails.objects.get(event_name=selected_event_name)
        except EventDetails.DoesNotExist:
            message = "Currently No Active Event"
            return render(request, 'chalan_views.html', {'message': message})

        event_products = EventProduct.objects.filter(event_id=event_details.event_id) \
                            .values('product_name') \
                            .annotate(count=Count('product_name'))
        sum_value=event_products.count()
        event_things = EventProduct.objects.filter(event_id=event_details.event_id)
        product_serial_numbers = defaultdict(list)

        for product in event_things:
            product_info = Product.objects.filter(qr_code=product.qr_code).first()
            if product_info:
                product_serial_numbers[product.product_name].append(product_info.serial_number)
        tempdata =temporaryaddeventdb.objects.filter(event_id=event_details.event_id)

        # Convert defaultdict to list of tuples for easier handling in the template
        product_serial_tuples = list(product_serial_numbers.items())
        product_configurations = {}
        for product in event_products:
            product_info = Product.objects.filter(name=product['product_name']).first()
            if product_info:
                product_configurations[product['product_name']] = product_info.configuration

        context = {
            'event_details': event_details,
            'event_products': event_products,
             'product_configurations': product_configurations,
            'product_serial_tuples': product_serial_tuples,
             'tempdata':tempdata,
            'blank_rows': '00',
            'tempdata':tempdata,
            'blank_rows': '00',
            'sum_value':sum_value,
        }

        return render(request, 'chalan.html', context)

    events = EventDetails.objects.filter(status=True).values_list('event_name', flat=True)
    context = {'events': events}
    return render(request, 'chalan_views.html', context)




# Take Product to Back
@login_required
def return_product_views(request):
    if request.method == 'POST':
        Event_name = request.POST.get('event')
        try:
            EventD=EventDetails.objects.get(event_name=Event_name)
            return redirect('return_product_to_office',EventD.event_id)
        except:
            pass
    events = EventDetails.objects.filter(status=True).values_list('event_name', flat=True)
    context = {'events': events}
    return render(request, 'return_product_views.html', context)


@login_required
def return_product_to_office(request, event_id):
    if not EventProduct.objects.filter(event_id=event_id, status=True).exists():
            # If all products have been returned, update the status of the event to False in EventDetails table
            event_details = EventDetails.objects.get(event_id=event_id)
            event_details.status = False
            event_details.save()
            return redirect("home")
    event_details = EventDetails.objects.get(event_id=event_id)
    if request.method == 'POST':
        qr_code = request.POST.get('qr_code')
        try:
            if EventProduct.objects.filter(qr_code=qr_code, status=False, event_id=event_id):
                message=f"With qr_code {qr_code} already added sucessfully"
                return render(request, 'return_product.html',{'message':message,'event_details':event_details})
            product = EventProduct.objects.get(qr_code=qr_code, status=True, event_id=event_id)
            product.status = False
            product.save()
            prod_qr=Product.objects.get(qr_code=qr_code)
            prod_qr.office_status="in_office"
            prod_qr.event_name=None
            prod_qr.save()
        except EventProduct.DoesNotExist:
            message=f"Qr Code {qr_code}  Does not exits for this event  ! can you rechek it "
            return render(request, 'return_product.html',{'message':message,'event_details':event_details})
        # Check if all products associated with the event have been returned
        message=f"Product with qr Code {qr_code} added Back to office successfully "
        return render(request, 'return_product.html', {'event_id': event_id,'event_details':event_details,'message':message})  # Redirect to a success page after returning the product

    return render(request, 'return_product.html', {'event_id': event_id,'event_details':event_details})


# Now i think is left that is view event

@login_required
def event_views(request):
    if request.method == 'POST':
        event_name = request.POST.get('event')
        try:
            event = EventDetails.objects.get(event_name=event_name)
            event_products = EventProduct.objects.filter(event_id=event.event_id)
            context = {
                'event_details': event,
                'event_products': event_products
            }
            return render(request, 'event_details.html', context)
        except EventDetails.DoesNotExist:
            message = f"Event with name {event_name} does not exist."
            return render(request, 'event_views.html', {'message': message})
    events = EventDetails.objects.filter().values_list('event_name', flat=True)
    context = {'events': events}
    return render(request, 'event_views.html', context)

@login_required
def event_views_active(request):
    if request.method == 'POST':
        event_name = request.POST.get('event')
        try:
            event = EventDetails.objects.get(event_name=event_name)
            event_products = EventProduct.objects.filter(event_id=event.event_id)
            Edit=True
            context = {
                'event_details': event,
                'event_products': event_products,
                'Edit':Edit

            }
            return render(request, 'event_details.html', context)
        except EventDetails.DoesNotExist:
            message = f"Event with name {event_name} does not exist."
            return render(request, 'event_views.html', {'message': message})
    events = EventDetails.objects.filter(status=True).values_list('event_name', flat=True)
    context = {'events': events}
    return render(request, 'event_views.html', context)


# Export ot excel
@login_required
def export_excel(request):
    if request.method == 'POST':
        selected_model = request.POST.get('model')  # Changed from request.GET to request.POST
        if selected_model == 'Product':
            queryset = Product.objects.all()
        elif selected_model == 'EventDetails':
            queryset = EventDetails.objects.all()
        elif selected_model == 'EventProduct':
            queryset = EventProduct.objects.all()
        else:
            return HttpResponse("Invalid model selection.")
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{selected_model}_data.xlsx"'
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = f"{selected_model} Data"
        # Write header row
        header_row =[field.name for field in queryset.model._meta.fields if not isinstance(field, AutoField)]
        worksheet.append(header_row)
        # Write data rows
        for obj in queryset:
            row = [getattr(obj, field.name) for field in queryset.model._meta.fields if not isinstance(field, AutoField)]
            worksheet.append(row)
        workbook.save(response)
        return response
    return render(request, 'ExportToExcel.html')
