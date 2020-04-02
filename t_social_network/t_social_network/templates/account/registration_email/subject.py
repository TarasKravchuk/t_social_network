import os

CURRENT_DIR = os.path.normpath(os.path.dirname(__file__))
EMAIL = os.path.join(CURRENT_DIR, 'email.html')
print(EMAIL)
subject = "t_social_network registration"
