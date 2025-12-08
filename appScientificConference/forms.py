from django import forms
from django.forms import ModelForm
from .models import Articulo, Autor, Track
from django.utils.translation import gettext_lazy as _
import re

class ArticuloForm(ModelForm):
    # Campos adicionales que NO están en el modelo
    confirmar_abstract = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'confirmar_abstract',
            'rows': 5,
            'placeholder': 'Reescribe el abstract para confirmar...',
            'class': 'form-control'
        }),
        required=False,
        label='Confirmar Abstract*'
    )
    
    terminos = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'id': 'terminos',
            'class': 'form-check-input'
        }),
        label=''
    )
    
    class Meta:
        model = Articulo
        fields = '__all__'  # Incluye todos los campos del modelo
        widgets = {
            'titulo': forms.TextInput(attrs={
                'id': 'titulo',
                'class': 'form-control',
                'placeholder': 'Título del artículo',
                'size': '40'
            }),
            'abstract': forms.Textarea(attrs={
                'id': 'abstract',
                'class': 'form-control xhtml-editor',
                'rows': 8,
                'cols': 50,
                'placeholder': 'Escribe el abstract aquí...'
            }),
            'track': forms.Select(attrs={
                'id': 'track',
                'class': 'form-control'
            }),
            'autores': forms.SelectMultiple(attrs={
                'id': 'autores',
                'class': 'form-control',
                'size': '5'
            })
        }
        labels = {
            'titulo': _('Título*'),
            'abstract': _('Abstract*'),
            'track': _('Track*'),
            'autores': _('Autores*'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar el queryset si es necesario
        self.fields['autores'].queryset = Autor.objects.all().order_by('nombre')
        self.fields['track'].queryset = Track.objects.all().order_by('nombre')
    
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if len(titulo) < 10:
            raise forms.ValidationError("El título debe tener al menos 10 caracteres.")
        return titulo
    
    def clean_abstract(self):
        abstract = self.cleaned_data.get('abstract')
        if len(abstract) < 100:
            raise forms.ValidationError("El abstract debe tener al menos 100 caracteres.")
        
        # Validar etiquetas HTML/XHTML básicas permitidas
        etiquetas_permitidas = ['p', 'br', 'b', 'i', 'u', 'strong', 'em', 'ul', 'ol', 'li']
        pattern = r'<(?!\/?(?:' + '|'.join(etiquetas_permitidas) + r')\b)[^>]+>'
        if re.search(pattern, abstract, re.IGNORECASE):
            raise forms.ValidationError(
                "Solo se permiten etiquetas HTML básicas: p, br, b, i, u, strong, em, ul, ol, li."
            )
        
        return abstract
    
    def clean(self):
        cleaned_data = super().clean()
        abstract = cleaned_data.get('abstract')
        confirmar_abstract = cleaned_data.get('confirmar_abstract')
        
        # Validar que los abstracts coincidan
        if abstract and confirmar_abstract and abstract != confirmar_abstract:
            self.add_error('confirmar_abstract', "Los abstracts no coinciden.")
        
        # Validar que haya al menos un autor
        autores = cleaned_data.get('autores')
        if not autores:
            self.add_error('autores', "Debe seleccionar al menos un autor.")
        elif len(autores) > 10:
            self.add_error('autores', "No se pueden seleccionar más de 10 autores.")
        
        return cleaned_data