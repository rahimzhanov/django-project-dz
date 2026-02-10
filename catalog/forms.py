from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product


class ProductForm(forms.ModelForm):
    # Константы с запрещенными словами
    FORBIDDEN_WORDS_NAME = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    FORBIDDEN_WORDS_DESCRIPTION = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Стилизация полей формы
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs.update({'class': 'form-control-file'})
            elif field_name == 'description':
                field.widget.attrs.update({'class': 'form-control', 'placeholder': 'Подробное описание товара'})
            elif field_name == 'is_published':
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

            if field.required:
                field.widget.attrs['required'] = 'required'

    def clean_name(self):
        """Валидация названия на запрещенные слова"""
        name = self.cleaned_data['name'].lower()

        for forbidden_word in self.FORBIDDEN_WORDS_NAME:
            if forbidden_word in name:
                raise ValidationError(
                    f'Название не должно содержать запрещенное слово: "{forbidden_word}"'
                )

        return self.cleaned_data['name']

    def clean_description(self):
        """Валидация описания на запрещенные слова"""
        description = self.cleaned_data['description'].lower()

        for forbidden_word in self.FORBIDDEN_WORDS_DESCRIPTION:
            if forbidden_word in description:
                raise ValidationError(
                    f'Описание не должно содержать запрещенное слово: "{forbidden_word}"'
                )

        return self.cleaned_data['description']

    def clean_price(self):
        """Валидация цены на отрицательные значения"""
        price = self.cleaned_data['price']

        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')

        if price == 0:
            raise ValidationError('Цена не может быть нулевой')

        return price

    def save(self, commit=True):
        """Сохраняем форму и устанавливаем владельца"""
        product = super().save(commit=False)

        # Если пользователь передан и продукт новый (нет pk)
        if self.user and not product.pk:
            product.owner = self.user

        if commit:
            product.save()

        return product