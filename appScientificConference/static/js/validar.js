// Función para borrar advertencias
function borrarWarn() {
    const warns = document.querySelectorAll('.error-message');
    warns.forEach(warn => warn.innerHTML = '');
    const preview = document.getElementById('preview');
    if (preview) preview.style.display = 'none';
    
    // También limpiar estilos de borde
    document.querySelectorAll('.form-control').forEach(input => {
        input.style.borderColor = '#bdc3c7';
    });
}

// Función para insertar etiquetas XHTML en el abstract
function insertarTag(tag) {
    const textarea = document.getElementById('id_abstract');
    if (!textarea) return;
    
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;
    
    if (tag === 'br') {
        textarea.value = text.substring(0, start) + '<br/>' + text.substring(end);
        textarea.selectionStart = textarea.selectionEnd = start + 5;
    } else {
        const selectedText = text.substring(start, end);
        const nuevaEtiqueta = '<' + tag + '>' + selectedText + '</' + tag + '>';
        textarea.value = text.substring(0, start) + nuevaEtiqueta + text.substring(end);
        textarea.selectionStart = start;
        textarea.selectionEnd = start + selectedText.length + tag.length * 2 + 5;
    }
    textarea.focus();
    
    // Disparar evento input para validación en tiempo real
    textarea.dispatchEvent(new Event('input'));
}

// Mostrar vista previa del abstract
function mostrarPreview() {
    const abstractInput = document.getElementById('id_abstract');
    const previewDiv = document.getElementById('preview-content');
    const previewContainer = document.getElementById('preview');
    
    if (!abstractInput || !previewDiv || !previewContainer) return;
    
    const abstract = abstractInput.value.trim();
    
    if (abstract) {
        previewDiv.innerHTML = abstract;
        previewContainer.style.display = 'block';
        
        // Desplazar suavemente a la vista previa
        previewContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } else {
        alert('Por favor, escribe algo en el abstract para ver la vista previa.');
    }
}

// Validar email (por si acaso)
function validarEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validar número
function validarNumero(numero) {
    return !isNaN(numero) && numero > 0;
}

// Validar etiquetas XHTML (verifica que estén balanceadas)
function validarXHTML(texto) {
    // Si no hay etiquetas, es válido
    if (!texto.includes('<')) return true;
    
    const etiquetasPermitidas = ['p', 'br', 'b', 'i', 'u', 'strong', 'em', 'ul', 'ol', 'li'];
    const regexEtiqueta = /<\/?([a-z][a-z0-9]*)[^>]*>/gi;
    const pila = [];
    let match;
    
    // Verificar etiquetas no permitidas
    while ((match = regexEtiqueta.exec(texto)) !== null) {
        const etiqueta = match[1].toLowerCase();
        if (!etiquetasPermitidas.includes(etiqueta)) {
            return false;
        }
    }
    
    // Verificar etiquetas balanceadas (resetear regex)
    const regexBalance = /<\/?([a-z][a-z0-9]*)[^>]*>/gi;
    const tags = texto.match(regexBalance) || [];
    
    for (let tag of tags) {
        const esCierre = tag.startsWith('</');
        const nombreEtiqueta = tag.replace(/[<\/>]/g, '');
        
        if (!esCierre) {
            // Etiqueta de apertura
            pila.push(nombreEtiqueta);
        } else {
            // Etiqueta de cierre
            if (pila.length === 0 || pila.pop() !== nombreEtiqueta) {
                return false;
            }
        }
    }
    
    return pila.length === 0;
}

// Validar formulario completo
function validarForm(soloValidar = false) {
    let valido = true;
    let mensajesError = [];
    
    // Limpiar advertencias anteriores
    borrarWarn();
    
    // Validar título
    const tituloInput = document.getElementById('id_titulo');
    if (tituloInput) {
        const titulo = tituloInput.value.trim();
        if (titulo.length < 10) {
            mensajesError.push('El título debe tener al menos 10 caracteres');
            mostrarError('id_titulo', 'El título debe tener al menos 10 caracteres');
            valido = false;
        }
    }
    
    // Validar track
    const trackSelect = document.getElementById('id_track');
    if (trackSelect) {
        if (!trackSelect.value) {
            mensajesError.push('Debe seleccionar un track');
            mostrarError('id_track', 'Debe seleccionar un track');
            valido = false;
        }
    }
    
    // Validar abstract
    const abstractInput = document.getElementById('id_abstract');
    if (abstractInput) {
        const abstract = abstractInput.value.trim();
        if (abstract.length < 100) {
            mensajesError.push(`El abstract debe tener al menos 100 caracteres (actual: ${abstract.length})`);
            mostrarError('id_abstract', `El abstract debe tener al menos 100 caracteres (actual: ${abstract.length})`);
            valido = false;
        } else if (!validarXHTML(abstract)) {
            mensajesError.push('El abstract tiene etiquetas XHTML mal formadas o no permitidas');
            mostrarError('id_abstract', 'El abstract tiene etiquetas XHTML mal formadas o no permitidas');
            valido = false;
        }
    }
    
    // Validar confirmación de abstract
    const confirmarAbstractInput = document.getElementById('id_confirmar_abstract');
    if (abstractInput && confirmarAbstractInput) {
        const abstract = abstractInput.value.trim();
        const confirmarAbstract = confirmarAbstractInput.value.trim();
        
        if (abstract !== confirmarAbstract) {
            mensajesError.push('Los abstracts no coinciden');
            mostrarError('id_confirmar_abstract', 'Los abstracts no coinciden');
            valido = false;
        }
    }
    
    // Validar autores
    const autoresSelect = document.getElementById('id_autores');
    if (autoresSelect) {
        const autoresSeleccionados = Array.from(autoresSelect.selectedOptions).length;
        if (autoresSeleccionados === 0) {
            mensajesError.push('Debe seleccionar al menos un autor');
            mostrarError('id_autores', 'Debe seleccionar al menos un autor');
            valido = false;
        }
    }
    
    // Validar términos
    const terminosCheckbox = document.getElementById('id_terminos');
    if (terminosCheckbox && !terminosCheckbox.checked) {
        mensajesError.push('Debe aceptar los términos y condiciones');
        mostrarError('id_terminos', 'Debe aceptar los términos y condiciones');
        valido = false;
    }
    
    // Mostrar resultado
    if (soloValidar) {
        if (valido) {
            alert('✅ ¡El formulario es válido! Puedes enviarlo.');
        } else {
            alert('❌ Hay errores en el formulario:\n\n' + mensajesError.join('\n'));
        }
        return false; // Para evitar envío si es solo validación
    }
    
    if (!valido) {
        alert('Por favor, corrija los errores antes de enviar:\n\n' + mensajesError.join('\n'));
        return false;
    }
    
    // Si todo está bien, deshabilitar botón de enviar para evitar doble envío
    const submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '⏳ Enviando...';
        setTimeout(() => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = submitBtn.innerHTML.replace('⏳ Enviando...', '💾 Guardar');
        }, 3000);
    }
    
    return true;
}

// Función auxiliar para mostrar errores en campos específicos
function mostrarError(campoId, mensaje) {
    const campo = document.getElementById(campoId);
    if (campo) {
        campo.style.borderColor = '#e74c3c';
        
        // Buscar o crear contenedor de error
        let errorDiv = campo.nextElementSibling;
        if (!errorDiv || !errorDiv.classList.contains('error-message')) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            campo.parentNode.insertBefore(errorDiv, campo.nextSibling);
        }
        errorDiv.textContent = mensaje;
    }
}

// Validación en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    // Configurar CSRF token para AJAX
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    
    // Validar título en tiempo real
    const tituloInput = document.getElementById('id_titulo');
    if (tituloInput) {
        tituloInput.addEventListener('blur', function() {
            const titulo = this.value.trim();
            if (titulo.length >= 10 && csrfToken) {
                // Validar unicidad con AJAX
                fetch('/validar-titulo/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({titulo: titulo})
                })
                .then(response => response.json())
                .then(data => {
                    if (!data.disponible) {
                        mostrarError('id_titulo', '⚠️ Este título ya está en uso');
                    } else {
                        // Limpiar error si existe
                        const errorDiv = tituloInput.nextElementSibling;
                        if (errorDiv && errorDiv.classList.contains('error-message')) {
                            errorDiv.textContent = '';
                        }
                        tituloInput.style.borderColor = '#2ecc71';
                    }
                })
                .catch(error => {
                    console.error('Error en validación AJAX:', error);
                });
            }
        });
    }
    
    // Validar abstract en tiempo real
    const abstractInput = document.getElementById('id_abstract');
    if (abstractInput) {
        abstractInput.addEventListener('input', function() {
            const texto = this.value.trim();
            if (texto.length > 0 && texto.length < 100) {
                this.style.borderColor = '#e74c3c';
            } else if (texto.length >= 100 && validarXHTML(texto)) {
                this.style.borderColor = '#2ecc71';
            } else {
                this.style.borderColor = '#bdc3c7';
            }
        });
    }
    
    // Validar coincidencia de abstracts en tiempo real
    const confirmarAbstractInput = document.getElementById('id_confirmar_abstract');
    if (abstractInput && confirmarAbstractInput) {
        function validarCoincidencia() {
            const abstract = abstractInput.value.trim();
            const confirmar = confirmarAbstractInput.value.trim();
            
            if (abstract && confirmar) {
                if (abstract === confirmar) {
                    confirmarAbstractInput.style.borderColor = '#2ecc71';
                } else {
                    confirmarAbstractInput.style.borderColor = '#e74c3c';
                }
            }
        }
        
        abstractInput.addEventListener('input', validarCoincidencia);
        confirmarAbstractInput.addEventListener('input', validarCoincidencia);
    }
    
    // Validar selección de autores
    const autoresSelect = document.getElementById('id_autores');
    if (autoresSelect) {
        autoresSelect.addEventListener('change', function() {
            if (this.selectedOptions.length > 0) {
                this.style.borderColor = '#2ecc71';
            } else {
                this.style.borderColor = '#e74c3c';
            }
        });
    }
    
    // Validar check de términos
    const terminosCheckbox = document.getElementById('id_terminos');
    if (terminosCheckbox) {
        terminosCheckbox.addEventListener('change', function() {
            const label = this.nextElementSibling;
            if (label && label.tagName === 'LABEL') {
                if (this.checked) {
                    label.style.color = '#2ecc71';
                } else {
                    label.style.color = '#e74c3c';
                }
            }
        });
    }
    
    // Asignar eventos a botones si existen
    const validarBtn = document.querySelector('button[onclick*="validarForm"]');
    if (validarBtn) {
        validarBtn.addEventListener('click', function(e) {
            e.preventDefault();
            validarForm(true);
        });
    }
    
    const previewBtn = document.querySelector('button[onclick*="mostrarPreview"]');
    if (previewBtn) {
        previewBtn.addEventListener('click', function(e) {
            e.preventDefault();
            mostrarPreview();
        });
    }
    
    // Validación antes de enviar el formulario
    const formulario = document.getElementById('articulo-form');
    if (formulario) {
        formulario.addEventListener('submit', function(e) {
            if (!validarForm(false)) {
                e.preventDefault();
            }
        });
    }
    
    // Asignar eventos a botones de toolbar
    document.querySelectorAll('.toolbar button').forEach(btn => {
        if (btn.onclick) {
            const oldOnClick = btn.onclick;
            btn.onclick = function(e) {
                e.preventDefault();
                oldOnClick.call(this);
            };
        }
    });
});