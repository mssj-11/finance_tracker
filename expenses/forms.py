# expenses/forms.py - Formularios para la aplicación "expenses"

from django import forms
from .models import Expense
from django.utils.translation import gettext_lazy as _

class ExpenseForm(forms.ModelForm):
    """
    Formulario basado en el modelo para la creación y edición de gastos.
    """
    class Meta:
        model = Expense
        fields = ['title', 'category', 'amount', 'date']
        labels = {
            'title': _("Título"),
            'category': _("Categoría"),
            'amount': _("Monto"),
            'date': _("Fecha"),
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _("Ejemplo: Cena en restaurante"),
                'maxlength': 255,
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _("Ejemplo: 50.75"),
                'step': '0.01',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        help_texts = {
            'title': _("Ingrese un título descriptivo para el gasto."),
            'amount': _("El monto debe ser mayor a cero."),
        }

    def clean_title(self):
        """
        Validación personalizada para el campo 'title'.
        """
        title = self.cleaned_data.get('title')
        if not title or not title.strip():
            raise forms.ValidationError(_("El título no puede estar vacío."))
        if len(title) > 255:
            raise forms.ValidationError(_("El título no puede exceder los 255 caracteres."))
        return title

    def clean_amount(self):
        """
        Validación personalizada para asegurar que el monto sea mayor a cero.
        """
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError(_("El monto debe ser mayor a cero."))
        return amount
