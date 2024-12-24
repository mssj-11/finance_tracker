# expenses/views.py - Vistas de la aplicación "expenses"

from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from xhtml2pdf import pisa
from django.contrib import messages
from django.views.generic import ListView
from django.views import View
from .models import Expense
from django.db.models import Sum
from .forms import ExpenseForm
from django.core.serializers.json import DjangoJSONEncoder
import json
import pandas as pd
import logging

# Configuración del logger para registrar eventos y errores
logger = logging.getLogger(__name__)


class ExpenseListView(ListView):
    """
    Vista que muestra una lista de todos los gastos.
    """
    model = Expense
    template_name = 'index.html'  # Plantilla principal
    context_object_name = 'expenses'

    def get_queryset(self):
        return Expense.objects.all()


class ExpenseCreateView(View):
    """
    Vista para la creación de un nuevo gasto.
    """
    template_name = 'add_expense.html'

    def get(self, request, *args, **kwargs):
        form = ExpenseForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ExpenseForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Gasto añadido exitosamente.")
                return redirect('expenses:index')  # Ruta actualizada
            except Exception as e:
                logger.error(f"Error al guardar el gasto: {e}")
                messages.error(request, "No se pudo guardar el gasto. Intente nuevamente.")
        return render(request, self.template_name, {'form': form})


class ExpenseUpdateView(View):
    """
    Vista para editar un gasto existente.
    """
    template_name = 'edit_expense.html'

    def get(self, request, expense_id, *args, **kwargs):
        expense = get_object_or_404(Expense, id=expense_id)
        form = ExpenseForm(instance=expense)
        return render(request, self.template_name, {'form': form, 'expense': expense})

    def post(self, request, expense_id, *args, **kwargs):
        expense = get_object_or_404(Expense, id=expense_id)
        form = ExpenseForm(request.POST, instance=expense)
        #print(form.instance.date)  # Verifica el valor de la fecha
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Gasto actualizado exitosamente.")
                return redirect('expenses:index')  # Ruta actualizada
            except Exception as e:
                logger.error(f"Error al actualizar el gasto: {e}")
                messages.error(request, "No se pudo actualizar el gasto. Intente nuevamente.")
        return render(request, self.template_name, {'form': form, 'expense': expense})


class ExpenseDeleteView(View):
    """
    Vista para eliminar un gasto existente.
    """
    def get(self, request, expense_id, *args, **kwargs):
        expense = get_object_or_404(Expense, id=expense_id)
        try:
            expense.delete()
            messages.success(request, "Gasto eliminado exitosamente.")
        except Exception as e:
            logger.error(f"Error al eliminar el gasto: {e}")
            messages.error(request, "No se pudo eliminar el gasto. Intente nuevamente.")
        return redirect('expenses:index')


class DashboardView(View):
    """
    Vista que muestra estadísticas generales de gastos. PARA EL TEMPLATE HTML
    """
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        try:
            # Total de gastos
            total_expenses = Expense.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

            # Todas las categorías existentes (ignorando duplicados)
            all_categories = (
                Expense.objects.values_list('category', flat=True)
                .distinct()
            )
            all_categories = sorted(set(category.upper() for category in all_categories))

            # Gastos totales por categoría
            expenses_by_category = (
                Expense.objects.values('category')
                .annotate(total_amount=Sum('amount'))
                .order_by('-total_amount')
            )

            # Categoría con el gasto más alto
            highest_spending_category = expenses_by_category[0] if expenses_by_category else None

            context = {
                'total_expenses': total_expenses,
                'all_categories': all_categories,
                #'expenses_by_category': expenses_by_category,
                'expenses_by_category': json.dumps(list(expenses_by_category), cls=DjangoJSONEncoder),
                'highest_spending_category': highest_spending_category,
            }

            return render(request, self.template_name, context)

        except Exception as e:
            logger.error(f"Error al cargar el dashboard: {e}")
            messages.error(request, "No se pudo cargar el panel de control.")
            return render(request, self.template_name, {
                'total_expenses': 0,
                'all_categories': [],
                'expenses_by_category': [],
                'highest_spending_category': None,
            })




######   Exportacion de datos ######

#   Reportes en Excel
def export_to_excel(request):
    # Obtener los datos del modelo
    expenses = Expense.objects.all().values('title', 'category', 'amount', 'date')

    # Crear un DataFrame de Pandas
    df = pd.DataFrame(expenses)

    # Renombrar columnas (opcional)
    df.rename(columns={
        'title': 'Título',
        'category': 'Categoría',
        'amount': 'Monto',
        'date': 'Fecha'
    }, inplace=True)

    # Configurar la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=expenses.xlsx'

    # Exportar a Excel
    df.to_excel(response, index=False, sheet_name='Gastos')

    return response


#   Reportes en PDF
def export_to_pdf(request):
    # Obtener los datos
    expenses = Expense.objects.all()

    # Renderizar la plantilla con los datos
    html = render_to_string('expenses_pdf.html', {'expenses': expenses})

    # Configurar la respuesta HTTP para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=expenses.pdf'

    # Convertir HTML a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response
