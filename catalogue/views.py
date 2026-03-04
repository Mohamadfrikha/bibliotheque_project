from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.db.models import Count, Sum,Q
from django.core.paginator import Paginator
# Create your views here.
from .models import Livre,Catalogue
def accueil(request):
    nouveautes = Livre.objects.all()[:5]
    # Catégories avec compteur de livres
    categories = Catalogue.objects.annotate(nb_livres=Count('livre')).filter(nb_livres__gt=0)
    # Statistiques
    stats = {
    'total_livres': Livre.objects.count(),
    'total_categories': categories.count(),
    'total_pages': Livre.objects.aggregate(
    total=Sum('nombre_pages')
    )['total'] or 0,
    }
    context = {
    'nouveautes': nouveautes,
    'categories': categories,
    'stats': stats,
    }
    return render(request, 'catalogue/accueil.html', context)
def catalogue(request):
    livres = Livre.objects.select_related('categorie').all()
    # Tri
    sort_by = request.GET.get('sort', '-date_ajout')
    valid_sorts = {
    'recent': '-date_ajout',
    'ancien': 'date_ajout',
    'titre': 'titre',
    'auteur': 'auteur',
    'pages_asc': 'nombre_pages',
    'pages_desc': '-nombre_pages',
    }
    if sort_by in valid_sorts:
        livres = livres.order_by(valid_sorts[sort_by])
    else:
        livres = livres.order_by(sort_by)
    # Pagination
    paginator = Paginator(livres, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'sort_by': request.GET.get('sort', 'recent'),
    }
    return render(request, 'catalogue/catalogue.html', context)
# Détail d'un livre
def livre_detail(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    
    context = {
    'livre': livre
    }
    return render(request, 'catalogue/livre_detail.html', context)

# Recherche avancée
def recherche(request):
    """
    Recherche avancée avec :
    - Recherche dans titre, auteur, résumé
    - Filtrage par catégorie
    - Suggestions si aucun résultat
    """
    query = request.GET.get('q', '')
    categorie_id = request.GET.get('categorie', '')
    livres = Livre.objects.all()

    if query:
        livres = livres.filter(
        Q(titre__icontains=query) |
        Q(auteur__icontains=query) |
        Q(resume__icontains=query)
        )
    if categorie_id:
        livres = livres.filter(categorie_id=categorie_id)
    # Suggestions si aucun résultat
    suggestions = []
    if query and not livres.exists():
        suggestions = Livre.objects.filter(
        titre__icontains=query
        )[:5]
    categories = Catalogue.objects.all()
    # Pagination
    paginator = Paginator(livres, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
    'page_obj': page_obj,
    'query': query,
    'categorie_id': categorie_id,
    'categories': categories,
    'suggestions': suggestions,
    'total_resultats': livres.count(),
    }
    return render(request, 'catalogue/recherche.html', context)