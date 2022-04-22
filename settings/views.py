from django.shortcuts import render


def custom_page_not_found_view(request, exception):
    return render(request, "partial_view/404.html", {})
