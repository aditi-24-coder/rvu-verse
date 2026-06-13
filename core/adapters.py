from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib import messages
from django.shortcuts import redirect


class RVUSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom adapter to validate RVU student emails during Google OAuth signup."""
    
    def pre_social_login(self, request, sociallogin):
        """
        Validate that the email belongs to an RVU student before allowing login.
        Instead of raising a raw ValidationError (which shows an ugly 500 page),
        we redirect back to the login page with a professional error message.
        """
        email = sociallogin.account.extra_data.get('email', '').lower()
        
        if not self._is_valid_rvu_email(email):
            messages.error(
                request,
                'google_auth_unauthorized'  # Special tag picked up by the login template
            )
            # Store the attempted email in the session for display purposes
            request.session['google_auth_failed_email'] = email
            raise ImmediateHttpResponse(redirect('login'))
    
    def save_user(self, request, sociallogin, form=None):
        """
        Save user after email validation passes.
        """
        # Validate email before saving
        email = sociallogin.account.extra_data.get('email', '').lower()
        if not self._is_valid_rvu_email(email):
            messages.error(
                request,
                'google_auth_unauthorized'
            )
            request.session['google_auth_failed_email'] = email
            raise ImmediateHttpResponse(redirect('login'))
        
        return super().save_user(request, sociallogin, form)
    
    @staticmethod
    def _is_valid_rvu_email(email):
        """
        Check if email ends with valid RVU student domain patterns.
        """
        allowed_endings = [
            'btech22@rvu.edu.in',
            'btech23@rvu.edu.in',
        ]
        return any(email.endswith(ending) for ending in allowed_endings)
