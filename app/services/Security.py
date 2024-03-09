from werkzeug.security import generate_password_hash, check_password_hash

# Fonction pour hacher et saler le mot de passe
def hash_password(password):
    return generate_password_hash(password)

# Fonction pour vérifier le mot de passe
def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)
