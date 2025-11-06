# API Design Standards

## RESTful Conventions

### URL Structure
GET /api/v1/users          # Obtener todos los usuarios
GET /api/v1/users/{id}     # Obtener usuario específico
POST /api/v1/users         # Crear nuevo usuario
PUT /api/v1/users/{id}     # Actualizar usuario completo
PATCH /api/v1/users/{id}   # Actualización parcial
DELETE /api/v1/users/{id}  # Eliminar usuario

### Response Format Standard
```python
# Respuesta exitosa
{
  "success": true,
  "data": {...},
  "meta": {
    "pagination": {...},
    "total": 100
  }
}

# Respuesta de error
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Datos inválidos",
    "details": {...}
  }
}
```
**Status Codes**
- 200: GET, PUT, PATCH exitosos
- 201: POST exitoso
- 204: DELETE exitoso
- 400: Bad Request
- 401: No autenticado
- 403: Sin permisos
- 404: No encontrado
- 422: Error de validación