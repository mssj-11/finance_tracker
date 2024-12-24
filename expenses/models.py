# expenses/models.py - Modelos de la aplicación "expenses"

from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Expense(models.Model):
    """
    Modelo que representa un gasto individual con campos como título, categoría, monto y fecha.
    """

    # Opciones de categorías disponibles para el gasto
    CATEGORY_CHOICES = [
        ('FOOD', _('Comida')),
        ('TRANSPORT', _('Transporte')),
        ('UTILITIES', _('Servicios Públicos')),
        ('ENTERTAINMENT', _('Entretenimiento')),
        ('OTHER', _('Otros')),
    ]

    # Título o descripción breve del gasto
    title = models.CharField(
        max_length=255,
        verbose_name=_("Título"),
        help_text=_("Breve descripción del gasto.")
    )

    # Categoría seleccionada entre las opciones predefinidas
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name=_("Categoría"),
        help_text=_("Categoría a la que pertenece el gasto.")
    )

    # Monto del gasto, validado para ser mayor que cero
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name=_("Monto"),
        help_text=_("Monto gastado. Debe ser mayor a cero.")
    )

    # Fecha del gasto (por defecto, fecha actual)
    date = models.DateField(
        default=timezone.now,
        verbose_name=_("Fecha"),
        help_text=_("Fecha en que se realizó el gasto.")
    )

    # Campos de fecha automáticos
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Creado en")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Actualizado en")
    )

    class Meta:
        """
        Configuración adicional del modelo.
        """
        verbose_name = _("Gasto")  # Nombre singular
        verbose_name_plural = _("Gastos")  # Nombre plural
        ordering = ['-date', '-created_at']  # Orden por fecha descendente y fecha de creación

    def __str__(self):
        """
        Representación legible del objeto Expense.
        """
        return f"{self.title} - ${self.amount} ({self.get_category_display()})"

    def clean(self):
        """
        Validaciones personalizadas antes de guardar el objeto.
        """
        from django.core.exceptions import ValidationError
        if not self.title.strip():
            raise ValidationError(_("El título no puede estar vacío."))

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para ejecutar validaciones personalizadas.
        """
        self.clean()  # Llamamos al método clean() para validar antes de guardar
        super().save(*args, **kwargs)
