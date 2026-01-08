from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from .models import Articulo, Autor, Track
from .forms import ArticuloForm


# =====================================
# INLINE: autores dentro de artículos
# =====================================
class AutorInline(admin.TabularInline):
    model = Articulo.autores.through
    extra = 1
    verbose_name = "Autor del artículo"
    verbose_name_plural = "Autores del artículo"
    can_delete = False
    max_num = 0  # Para modo solo lectura


# =====================================
# ADMIN DE TRACK
# =====================================
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion_corta")
    search_fields = ("nombre",)
    ordering = ("nombre",)

    def descripcion_corta(self, obj):
        return (obj.descripcion[:50] + "...") if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = "Descripción"


# =====================================
# ADMIN DE AUTOR
# =====================================
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "afiliacion", "imagen_preview")
    search_fields = ("nombre", "afiliacion")
    list_filter = ("afiliacion",)
    ordering = ("nombre",)

    readonly_fields = ("imagen_preview",)

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width:60px; height:60px; border-radius:4px;" />', obj.imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = "Foto"


# =====================================
# ADMIN DE ARTÍCULO - VERSIÓN CORREGIDA
# =====================================
@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    # Form personalizado SOLO para usuarios que pueden editar
    form = ArticuloForm
    
    # ---------------------------
    # LISTADO
    # ---------------------------
    list_display = ("titulo", "track", "lista_autores", "abstract_corto")
    search_fields = ("titulo", "abstract", "autores__nombre")
    list_filter = ("track",)
    ordering = ("track", "titulo")
    list_per_page = 20

    # ---------------------------
    # DETALLE / FORMULARIO
    # ---------------------------
    fieldsets = (
        ("Información básica", {
            "fields": ("titulo", "abstract"),
            "classes": ("wide",)
        }),
        ("Clasificación", {
            "fields": ("track", "autores"),
            "classes": ("collapse",)
        }),
    )

    # ---------------------------
    # METODOS PERSONALIZADOS
    # ---------------------------
    def lista_autores(self, obj):
        return ", ".join([a.nombre for a in obj.autores.all()])
    lista_autores.short_description = "Autores"

    def abstract_corto(self, obj):
        return obj.abstract[:60] + "..." if len(obj.abstract) > 60 else obj.abstract
    abstract_corto.short_description = "Resumen"

    # ============================================
    # ACCIONES personalizadas
    # ============================================
    @admin.action(description="Marcar artículos como aprobados")
    def marcar_aprobado(self, request, queryset):
        # Solo para usuarios que no son revisores
        if not self._es_revisor(request):
            updated = queryset.update(abstract=queryset.first().abstract + "\n\n[Aprobado]")
            self.message_user(request, f"{updated} artículos marcados como aprobados")
    actions = ["marcar_aprobado"]

    # ============================================
    # MÉTODOS HELPER
    # ============================================
    def _es_revisor(self, request):
        """Método helper para verificar si el usuario es revisor"""
        return request.user.groups.filter(name="Revisor").exists()

    # ============================================
    # PERMISOS Y COMPORTAMIENTO POR ROL
    # ============================================

    def get_queryset(self, request):
        """Obtener queryset base"""
        qs = super().get_queryset(request)
        # Si es revisor, puede ver todos los artículos
        return qs

    def get_inlines(self, request, obj=None):
        """Mostrar/ocultar inlines según permisos"""
        if self._es_revisor(request):
            # Para revisores, mostramos un inline de solo lectura
            return [AutorInlineReadOnly]
        return [AutorInline]

    def get_readonly_fields(self, request, obj=None):
        """Campos de solo lectura"""
        if self._es_revisor(request):
            # Para revisores, TODOS los campos son de solo lectura
            return [f.name for f in self.model._meta.fields] + ['autores']
        return super().get_readonly_fields(request, obj)

    def get_fieldsets(self, request, obj=None):
        """Personalizar fieldsets según rol"""
        if self._es_revisor(request):
            # Para revisores, mostrar más campos en la vista de detalle
            return (
                ("Información básica", {
                    "fields": ("titulo", "abstract"),
                    "classes": ("wide",)
                }),
                ("Clasificación", {
                    "fields": ("track", "autores"),
                    "classes": ("collapse",)
                }),
            )
        return super().get_fieldsets(request, obj)

    def has_add_permission(self, request):
        """Permiso para agregar"""
        if self._es_revisor(request):
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        """Permiso para cambiar - DEVOLVEMOS True para que puedan VER"""
        # IMPORTANTE: Esto permite acceder a la vista de detalle
        # Los campos serán de solo lectura via get_readonly_fields
        return True

    def has_delete_permission(self, request, obj=None):
        """Permiso para eliminar"""
        if self._es_revisor(request):
            return False
        return super().has_delete_permission(request, obj)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Sobreescribir la vista de cambio para revisores"""
        extra_context = extra_context or {}
        
        if self._es_revisor(request):
            # Configurar contexto para vista de solo lectura
            extra_context.update({
                'show_save': False,
                'show_save_and_continue': False,
                'show_save_and_add_another': False,
                'show_delete': False,
                'title': f"Ver {self.model._meta.verbose_name}",
                'is_readonly': True,
                'readonly': True,
            })
            
            # Deshabilitar todos los campos en el template
            self.readonly_fields = self.get_readonly_fields(request)
            
        return super().change_view(request, object_id, form_url, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        """Vista del formulario de cambio - manejar POST para revisores"""
        if self._es_revisor(request) and request.method == 'POST':
            # Si un revisor intenta enviar un formulario, redirigir con mensaje de error
            messages.error(request, "Los revisores no tienen permiso para modificar artículos.")
            return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % (
                self.model._meta.app_label,
                self.model._meta.model_name
            )))
        
        return super().changeform_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        """Vista para agregar - bloquear para revisores"""
        if self._es_revisor(request):
            messages.error(request, "Los revisores no tienen permiso para agregar artículos.")
            return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % (
                self.model._meta.app_label,
                self.model._meta.model_name
            )))
        return super().add_view(request, form_url, extra_context)

    def response_change(self, request, obj):
        """Respuesta después de cambiar - bloquear para revisores"""
        if self._es_revisor(request):
            messages.error(request, "Los revisores no tienen permiso para modificar artículos.")
            return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % (
                self.model._meta.app_label,
                self.model._meta.model_name
            )))
        return super().response_change(request, obj)


# =====================================
# INLINE DE SOLO LECTURA PARA REVISORES
# =====================================
class AutorInlineReadOnly(admin.TabularInline):
    model = Articulo.autores.through
    verbose_name = "Autor del artículo"
    verbose_name_plural = "Autores del artículo"
    
    # Configuración para solo lectura
    can_delete = False
    extra = 0
    max_num = 0
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_readonly_fields(self, request, obj=None):
        # Todos los campos son de solo lectura
        return [field.name for field in self.model._meta.fields]
    
    def get_fields(self, request, obj=None):
        # Mostrar solo el campo autor
        return ['autor']
    
    def get_queryset(self, request):
        # Optimizar la consulta
        return super().get_queryset(request).select_related('autor')