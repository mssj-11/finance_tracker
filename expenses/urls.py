# expenses/urls.py - Rutas específicas de la aplicación "expenses"

from django.urls import path
from .views import ExpenseListView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView, DashboardView

# Definir el namespace 'expenses'
app_name = "expenses"

urlpatterns = [
    # Ruta para la página principal de la lista de gastos
    path('', ExpenseListView.as_view(), name='index'),

    # Ruta para añadir un nuevo gasto
    path('add/', ExpenseCreateView.as_view(), name='add_expense'),

    # Ruta para editar un gasto existente
    path('edit/<int:expense_id>/', ExpenseUpdateView.as_view(), name='edit_expense'),

    # Ruta para eliminar un gasto existente
    path('delete/<int:expense_id>/', ExpenseDeleteView.as_view(), name='delete_expense'),

    # Ruta para ver el panel de estadísticas
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
