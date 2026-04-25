"""
Request validation decorators for Flask routes.

Provides decorators to validate and sanitize request inputs before
they reach route handlers, preventing SQL injection and other attacks.
"""

from functools import wraps
from flask import request, jsonify
from utils.security import (
    validate_string_input,
    validate_integer,
    validate_float,
    validate_boolean,
    detect_sql_injection_attempt,
    validate_email_format,
    validate_phone,
    validate_coordinates
)
import logging

logger = logging.getLogger(__name__)


def validate_form_data(validations):
    """
    Decorator to validate form data before route execution.

    Usage:
        @validate_form_data({
            'name': {'type': 'string', 'required': True, 'max_length': 200},
            'rating': {'type': 'int', 'min': 1, 'max': 5},
            'email': {'type': 'email', 'required': True}
        })
        def create_review():
            # request.validated_data contains sanitized values
            name = request.validated_data['name']

    Args:
        validations: Dict mapping field names to validation rules

    Returns:
        Decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Skip validation for GET requests
            if request.method == 'GET':
                return f(*args, **kwargs)

            validated_data = {}
            errors = []

            for field, rules in validations.items():
                raw_value = request.form.get(field) or request.values.get(field)
                is_required = rules.get('required', False)

                # Check if required field is missing
                if is_required and not raw_value:
                    errors.append(f"{field} is required")
                    continue

                # Skip validation if field is not provided and not required
                if not raw_value and not is_required:
                    validated_data[field] = None
                    continue

                # Validate based on type
                field_type = rules.get('type', 'string')

                if field_type == 'string':
                    is_valid, error_msg = validate_string_input(
                        raw_value,
                        min_length=rules.get('min_length', 0),
                        max_length=rules.get('max_length', 500),
                        allowed_pattern=rules.get('pattern'),
                        block_sql_injection=rules.get('block_sql_injection', True)
                    )
                    if is_valid:
                        validated_data[field] = raw_value
                    else:
                        errors.append(f"{field}: {error_msg}")

                elif field_type == 'email':
                    if not validate_email_format(raw_value):
                        errors.append(f"{field}: Invalid email format")
                    else:
                        validated_data[field] = raw_value

                elif field_type == 'phone':
                    if not validate_phone(raw_value):
                        errors.append(f"{field}: Invalid phone number")
                    else:
                        validated_data[field] = raw_value

                elif field_type == 'int':
                    is_valid, int_value, error_msg = validate_integer(
                        raw_value,
                        min_value=rules.get('min'),
                        max_value=rules.get('max')
                    )
                    if is_valid:
                        validated_data[field] = int_value
                    else:
                        errors.append(f"{field}: {error_msg}")

                elif field_type == 'float':
                    is_valid, float_value, error_msg = validate_float(
                        raw_value,
                        min_value=rules.get('min'),
                        max_value=rules.get('max')
                    )
                    if is_valid:
                        validated_data[field] = float_value
                    else:
                        errors.append(f"{field}: {error_msg}")

                elif field_type == 'bool':
                    is_valid, bool_value = validate_boolean(raw_value)
                    if is_valid:
                        validated_data[field] = bool_value
                    else:
                        errors.append(f"{field}: Invalid boolean value")

            # If there are validation errors, return error response
            if errors:
                logger.warning(f"Validation failed: {', '.join(errors)}")
                
                # Return JSON for API requests, otherwise render error page
                if request.is_json or request.path.startswith('/api/'):
                    return jsonify({
                        'success': False,
                        'errors': errors
                    }), 400
                else:
                    # For form submissions, flash error and redirect
                    from flask import flash, redirect, url_for
                    for error in errors:
                        flash(error, 'error')
                    return redirect(request.referrer or url_for('public.index'))

            # Attach validated data to request
            request.validated_data = validated_data
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_json_input(validations):
    """
    Decorator to validate JSON request body before route execution.

    Usage:
        @validate_json_input({
            'name': {'type': 'string', 'required': True, 'max_length': 200},
            'price': {'type': 'float', 'min': 0}
        })
        def create_item():
            data = request.validated_data

    Args:
        validations: Dict mapping field names to validation rules

    Returns:
        Decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Skip validation for GET requests
            if request.method == 'GET':
                return f(*args, **kwargs)

            if not request.is_json:
                return jsonify({'success': False, 'errors': ['Request must be JSON']}), 400

            json_data = request.get_json()
            validated_data = {}
            errors = []

            for field, rules in validations.items():
                raw_value = json_data.get(field)
                is_required = rules.get('required', False)

                # Check if required field is missing
                if is_required and raw_value is None:
                    errors.append(f"{field} is required")
                    continue

                # Skip validation if field is not provided and not required
                if raw_value is None and not is_required:
                    validated_data[field] = None
                    continue

                # Validate based on type
                field_type = rules.get('type', 'string')

                if field_type == 'string':
                    is_valid, error_msg = validate_string_input(
                        str(raw_value),
                        min_length=rules.get('min_length', 0),
                        max_length=rules.get('max_length', 500),
                        allowed_pattern=rules.get('pattern'),
                        block_sql_injection=rules.get('block_sql_injection', True)
                    )
                    if is_valid:
                        validated_data[field] = raw_value
                    else:
                        errors.append(f"{field}: {error_msg}")

                elif field_type == 'email':
                    if not validate_email_format(str(raw_value)):
                        errors.append(f"{field}: Invalid email format")
                    else:
                        validated_data[field] = raw_value

                elif field_type == 'int':
                    is_valid, int_value, error_msg = validate_integer(
                        raw_value,
                        min_value=rules.get('min'),
                        max_value=rules.get('max')
                    )
                    if is_valid:
                        validated_data[field] = int_value
                    else:
                        errors.append(f"{field}: {error_msg}")

                elif field_type == 'float':
                    is_valid, float_value, error_msg = validate_float(
                        raw_value,
                        min_value=rules.get('min'),
                        max_value=rules.get('max')
                    )
                    if is_valid:
                        validated_data[field] = float_value
                    else:
                        errors.append(f"{field}: {error_msg}")

            # If there are validation errors, return error response
            if errors:
                logger.warning(f"JSON validation failed: {', '.join(errors)}")
                return jsonify({
                    'success': False,
                    'errors': errors
                }), 400

            # Attach validated data to request
            request.validated_data = validated_data
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_query_params(validations):
    """
    Decorator to validate query parameters (whitelist approach with optional rules).

    Usage:
        @validate_query_params({
            'page': {'type': 'int', 'min': 1},
            'q': {'type': 'string', 'max_length': 200},
            'category': {'type': 'string', 'max_length': 50}
        })
        def list_items():
            page = request.validated_params.get('page', 1)

    Args:
        validations: List of allowed parameter names OR Dict mapping names to rules
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            validated_params = {}
            errors = []
            
            is_dict = isinstance(validations, dict)
            allowed_list = validations.keys() if is_dict else validations

            # Check for disallowed parameters
            for param in request.args:
                if param not in allowed_list:
                    errors.append(f"Parameter '{param}' is not allowed")
                    continue

                raw_value = request.args.get(param)
                if not raw_value:
                    continue

                if is_dict:
                    rules = validations[param]
                    field_type = rules.get('type', 'string')

                    if field_type == 'int':
                        is_valid, int_value, error_msg = validate_integer(
                            raw_value,
                            min_value=rules.get('min'),
                            max_value=rules.get('max')
                        )
                        if is_valid:
                            validated_params[param] = int_value
                        else:
                            errors.append(f"{param}: {error_msg}")
                    
                    elif field_type == 'string':
                        is_valid, error_msg = validate_string_input(
                            raw_value,
                            max_length=rules.get('max_length', 500),
                            block_sql_injection=rules.get('block_sql_injection', True)
                        )
                        if is_valid:
                            validated_params[param] = raw_value
                        else:
                            errors.append(f"{param}: {error_msg}")
                    else:
                        # Fallback for other types
                        if detect_sql_injection_attempt(raw_value):
                            errors.append(f"{param}: Invalid characters detected")
                        else:
                            validated_params[param] = raw_value
                else:
                    # Legacy list-based behavior
                    if param in ['page', 'per_page']:
                        is_valid, int_value, error_msg = validate_integer(raw_value, min_value=1)
                        if is_valid:
                            validated_params[param] = int_value
                        else:
                            errors.append(f"{param}: {error_msg}")
                    elif detect_sql_injection_attempt(raw_value):
                        errors.append(f"{param}: Invalid characters detected")
                    else:
                        validated_params[param] = raw_value

            if errors:
                logger.warning(f"Query param validation failed: {', '.join(errors)}")
                
                if request.is_json or request.path.startswith('/api/'):
                    return jsonify({
                        'success': False,
                        'errors': errors
                    }), 400
                else:
                    from flask import flash, redirect, url_for
                    for error in errors:
                        flash(error, 'error')
                    return redirect(request.referrer or url_for('public.index'))

            request.validated_params = validated_params
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_coordinates_fields(lat_field='latitude', lng_field='longitude'):
    """
    Decorator to validate geographic coordinates.

    Usage:
        @validate_coordinates_fields()
        def create_attraction():
            lat = request.validated_data['latitude']
            lng = request.validated_data['longitude']

    Args:
        lat_field: Name of latitude field
        lng_field: Name of longitude field

    Returns:
        Decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            lat = request.form.get(lat_field) or request.values.get(lat_field)
            lng = request.form.get(lng_field) or request.values.get(lng_field)

            if lat and lng:
                try:
                    lat_float = float(lat)
                    lng_float = float(lng)
                    
                    if not validate_coordinates(lat_float, lng_float):
                        return jsonify({
                            'success': False,
                            'errors': ['Invalid coordinates (must be within valid range)']
                        }), 400
                except ValueError:
                    return jsonify({
                        'success': False,
                        'errors': ['Invalid coordinate format']
                    }), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator
