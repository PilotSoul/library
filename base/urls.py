from django.urls import path

from .views import (
    VisitorCreateView,
    VisitorDestroyView,
    DepartmentCreateView,
    DepartmentRetrieveDestroyView,
    DepartmentListView,
    LoanBookView,
    ReturnBookView,
    VisitorRetrieveView,
    VisitorListView,
    BookListView,
)

app_name = "base"

urlpatterns = [
    path("visitor/new", VisitorCreateView.as_view(), name="visitor-new"),
    path("visitor/<int:pk>", VisitorDestroyView.as_view(), name="visitor-single"),
    path("visitor/list/books-loaned", VisitorListView.as_view(), name="visitor-list"),
    path("department/new", DepartmentCreateView.as_view(), name="department-new"),
    path("department/<int:pk>", DepartmentRetrieveDestroyView.as_view(), name="department-single"),
    path("department/list", DepartmentListView.as_view(), name="department-list"),
    path('loan/<int:book_id>/<int:visitor_id>/', LoanBookView.as_view(), name='loan-book'),
    path('return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),
    path("books/visitor/<int:pk>", VisitorRetrieveView.as_view(), name="visitor-get"),
    path("books/list/", BookListView.as_view(), name="book-list"),
]
