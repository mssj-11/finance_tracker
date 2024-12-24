# expenses/tests.py - Pruebas para la aplicación "expenses"

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Expense
from .forms import ExpenseForm

class ExpenseModelTest(TestCase):
    """
    Pruebas para el modelo Expense.
    """

    def setUp(self):
        self.expense = Expense.objects.create(
            title="Cena en restaurante",
            category="FOOD",
            amount=50.75,
            date=timezone.now()
        )

    def test_expense_creation(self):
        """
        Verifica que un gasto se crea correctamente.
        """
        self.assertEqual(self.expense.title, "Cena en restaurante")
        self.assertEqual(self.expense.category, "FOOD")
        self.assertEqual(float(self.expense.amount), 50.75)

    def test_expense_str_representation(self):
        """
        Verifica la representación en cadena del modelo Expense.
        """
        expected_str = f"{self.expense.title} - ${self.expense.amount} ({self.expense.get_category_display()})"
        self.assertEqual(str(self.expense), expected_str)

    def test_expense_ordering(self):
        """
        Verifica que los gastos se ordenan correctamente.
        """
        Expense.objects.create(
            title="Pago de electricidad",
            category="UTILITIES",
            amount=30.00,
            date=timezone.now() - timezone.timedelta(days=1)
        )
        expenses = Expense.objects.all()
        self.assertEqual(expenses.first(), self.expense)  # Última fecha aparece primero


class ExpenseFormTest(TestCase):
    """
    Pruebas para el formulario ExpenseForm.
    """

    def test_valid_form(self):
        """
        Verifica que un formulario válido pase la validación.
        """
        form_data = {
            'title': "Compra de libros",
            'category': "OTHER",
            'amount': 20.00,
            'date': timezone.now().date()
        }
        form = ExpenseForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_empty_title(self):
        """
        Verifica que un formulario con título vacío no pase la validación.
        """
        form_data = {
            'title': "",
            'category': "FOOD",
            'amount': 15.00,
            'date': timezone.now().date()
        }
        form = ExpenseForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class ExpenseViewTest(TestCase):
    """
    Pruebas para las vistas de la aplicación "expenses".
    """

    def setUp(self):
        self.client = Client()
        self.expense = Expense.objects.create(
            title="Gasolina",
            category="TRANSPORT",
            amount=40.00,
            date=timezone.now()
        )

    def test_expense_list_view(self):
        """
        Verifica que la vista de lista de gastos se cargue correctamente.
        """
        response = self.client.get(reverse('expenses-index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/index.html')
        self.assertContains(response, "Gasolina")

    def test_expense_create_view(self):
        """
        Verifica que la vista de creación de gastos funcione correctamente.
        """
        response = self.client.post(reverse('add-expense'), {
            'title': "Compra de ropa",
            'category': "OTHER",
            'amount': 100.00,
            'date': timezone.now().date()
        })
        self.assertEqual(response.status_code, 302)  # Redirección exitosa
        self.assertEqual(Expense.objects.count(), 2)

    def test_expense_update_view(self):
        """
        Verifica que la vista de actualización de gastos funcione correctamente.
        """
        response = self.client.post(reverse('edit-expense', args=[self.expense.id]), {
            'title': "Gasolina Premium",
            'category': "TRANSPORT",
            'amount': 50.00,
            'date': timezone.now().date()
        })
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.title, "Gasolina Premium")
        self.assertEqual(float(self.expense.amount), 50.00)

    def test_expense_delete_view(self):
        """
        Verifica que la vista de eliminación de gastos funcione correctamente.
        """
        response = self.client.post(reverse('delete-expense', args=[self.expense.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Expense.objects.count(), 0)

    def test_dashboard_view(self):
        """
        Verifica que el panel de control muestre estadísticas correctamente.
        """
        response = self.client.get(reverse('expenses-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "40.00")
