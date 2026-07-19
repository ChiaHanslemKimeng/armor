from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import ProductReview


def reviews_list_view(request):
    """Customer Reviews & Testimonials across Glocks And Armor."""
    reviews = ProductReview.objects.filter(is_approved=True).select_related('product', 'user')[:20]
    return render(request, 'reviews/list.html', {'reviews': reviews})


def helpful_vote_view(request, review_id):
    """HTMX endpoint incrementing helpful vote and returning badge."""
    review = get_object_or_404(ProductReview, id=review_id)
    review.helpful_votes += 1
    review.save(update_fields=['helpful_votes'])
    return HttpResponse(f'<span class="badge bg-success bg-opacity-10 text-success"><i class="bi bi-hand-thumbs-up-fill"></i> Helpful ({review.helpful_votes})</span>')

