from django import template
from django.conf import settings
from urllib.parse import urlsplit

register = template.Library()

@register.simple_tag(takes_context=True)
def current_path_in_language(context, lang_code):
    """
    Devuelve la URL actual pero con el prefijo de idioma adecuado
    para funcionar con i18n_patterns.
    """
    request = context.get('request')
    if not request:
        return '/'

    full = request.get_full_path()  # incluye query string
    split = urlsplit(full)
    path = split.path or '/'
    lang_codes = [code for code, _ in settings.LANGUAGES]

    parts = path.split('/')
    first = parts[1] if len(parts) > 1 else ''

    # quitar prefijo de idioma actual si existe
    if first in lang_codes:
        rest = '/' + '/'.join(parts[2:]) if len(parts) > 2 else '/'
    else:
        rest = path

    # construir nuevo path con el idioma solicitado
    if lang_code == settings.LANGUAGE_CODE:
        # idioma por defecto: sin prefijo
        new_path = rest
    else:
        if rest == '/':
            new_path = f'/{lang_code}/'
        else:
            new_path = f'/{lang_code}{rest}'

    # volver a añadir la query string si la hubiera
    return new_path + (f'?{split.query}' if split.query else '')