from uuid import UUID

def user_id_to_str(user_id):
    """Конвертирует UUID в строку для тестов"""
    if isinstance(user_id, UUID):
        return str(user_id)
    return user_id

def str_to_user_id(user_id_str):
    """Конвертирует строку в UUID для тестов (если нужно)"""
    if isinstance(user_id_str, str) and len(user_id_str) == 36:
        try:
            return UUID(user_id_str)
        except ValueError:
            return user_id_str
    return user_id_str