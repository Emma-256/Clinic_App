from django import forms
from .models import InventoryItem, DrugCategory, Formulation, StorageCondition, SaleUnit


class InventoryItemForm(forms.ModelForm):
    """
    Form for creating / editing an InventoryItem.

    The `clinic` field is intentionally excluded from the rendered form —
    it is injected automatically by the view using the URL's `pk` parameter,
    so the user never sees or touches it.
    """

    class Meta:
        model  = InventoryItem
        fields = [
            "brand_name",
            "generic_name",
            "drug_categories",
            "formulation",
            "storage_condition",
            "reorder_level",
            "stock_target",
            "sale_price",
            "sale_unit",
            "discontinued",
            "pause_stocking",
            "is_active",
            # NOTE: `clinic` is NOT in this list — it is set in the view.
        ]

        widgets = {
            # Text fields — styled via CSS class in the template;
            # plain attrs here keep the form.py clean.
            "brand_name": forms.TextInput(attrs={
                "autocomplete": "off",
            }),
            "generic_name": forms.TextInput(attrs={
                "autocomplete": "off",
            }),

            # Multi-select rendered as pill checkboxes in the template,
            # so the widget itself just needs to pass the right name.
            "drug_categories": forms.CheckboxSelectMultiple(),

            # Dropdowns
            "formulation":       forms.Select(),
            "storage_condition": forms.Select(),
            "sale_unit":         forms.Select(),

            # Numbers
            "reorder_level": forms.NumberInput(attrs={"min": 0}),
            "stock_target":  forms.NumberInput(attrs={"min": 1}),
            "sale_price":    forms.NumberInput(attrs={"step": "0.01", "min": "0"}),

            # Boolean toggles — rendered as custom toggle switches in the template
            "discontinued":    forms.CheckboxInput(),
            "pause_stocking":  forms.CheckboxInput(),
            "is_active":       forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        # Pop the clinic kwarg injected by the view (if present).
        # We store it so we can assign it during save() without
        # requiring the user to select it.
        self._clinic = kwargs.pop("clinic", None)
        super().__init__(*args, **kwargs)

        # Sort all FK / M2M dropdowns alphabetically for usability
        self.fields["drug_categories"].queryset = DrugCategory.objects.order_by("name")
        self.fields["formulation"].queryset      = Formulation.objects.order_by("name")
        self.fields["storage_condition"].queryset = StorageCondition.objects.order_by("name")
        self.fields["sale_unit"].queryset         = SaleUnit.objects.order_by("name")

        # Make certain fields optional at the form level
        # (reorder_level and stock_target may legitimately be blank)
        self.fields["reorder_level"].required    = False
        self.fields["stock_target"].required     = False
        self.fields["storage_condition"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Inject the clinic that was passed in from the view
        if self._clinic is not None:
            instance.clinic = self._clinic

        if commit:
            instance.save()
            self.save_m2m()

        return instance