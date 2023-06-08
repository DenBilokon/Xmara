from django.shortcuts import render


def main_mf(request):
    return render(request, 'file_manager/index.html')

