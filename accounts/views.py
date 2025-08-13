from django.shortcuts import render

def landing_page(request):
    """ 
    This view will return static landing page 
    Args:
        - request from users
    Returns:
        - Render landing page
    """
    return render(request, 'accounts/landingpage.html')