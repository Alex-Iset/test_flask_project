def validate(user):
    errors = {}
    if not user['username']:
        errors['username'] = 'The "username" field is not filled in.'
    if not user['email']:
        errors['email'] = 'The "email" field is not filled in.'
    return errors
