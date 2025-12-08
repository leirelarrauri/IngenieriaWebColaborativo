from django.contrib import admin
from django.utils.html import format_html
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
# ADMIN DE ARTÍCULO
# =====================================
@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    form = ArticuloForm
    inlines = [AutorInline]

    # ---------------------------
    # LISTADO
    # ---------------------------
    list_display = ("titulo", "track", "lista_autores", "abstract_corto")
    search_fields = ("titulo", "abstract", "autores__nombre")
    list_filter = ("track", "autores")
    ordering = ("track", "titulo")
    list_per_page = 20
    autocomplete_fields = ("track", "autores")

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
        queryset.update(abstract=queryset.first().abstract + "\n\n[Aprobado]")
    actions = ["marcar_aprobado"]

    # ============================================
    # PERMISOS POR ROL
    # ============================================

    def has_add_permission(self, request):
        # Revisor NO puede crear
        if request.user.groups.filter(name="Revisor").exists():
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        # Revisor NO puede editar
        if request.user.groups.filter(name="Revisor").exists():
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Solo Administrador General puede borrar
        if not request.user.groups.filter(name="Administrador General").exists():
            return False
        return True

    def get_readonly_fields(self, request, obj=None):
        # Revisor ve todo solo lectura
        if request.user.groups.filter(name="Revisor").exists():
            return [f.name for f in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

    def get_inlines(self, request, obj):
        # Revisor NO ve autores
        if request.user.groups.filter(name="Revisor").exists():
            return []
        return [AutorInline]
