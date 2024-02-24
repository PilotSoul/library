from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    RetrieveDestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)

from base.models import Visitor, Department, Loan, Book
from django.db.models import Prefetch, Count

from base.serializers import (
    VisitorSerializer,
    DepartmentSerializer,
    BookLoanSerializer,
    VisitorRetrieveSerializer,
    VisitorListSerializer,
    BookSerializer,
)

from django_filters.rest_framework import FilterSet, DjangoFilterBackend, BooleanFilter


# Visitors Views -------------------------------------
class VisitorCreateView(CreateAPIView):
    """
    Точка для добавления посетителей библиотеки
    """

    serializer_class = VisitorSerializer
    queryset = Visitor.objects.all()


class VisitorDestroyView(DestroyAPIView):
    """
    Точка для удаления посетителя библиотеки
    """

    serializer_class = VisitorSerializer
    queryset = Visitor.objects.all()


class VisitorRetrieveView(RetrieveAPIView):
    """
    Точка для получения
    полной информации о посетителе библиотеки
    """

    serializer_class = VisitorRetrieveSerializer
    queryset = Visitor.objects.prefetch_related(
        Prefetch(
            "loan_set",
            queryset=Loan.objects.only(
                "book_id",
                "book__title",
            ).filter(
                return_date=None
            ).select_related(
                "book"
            ),
        )
    ).only(
        'id',
        'family_name',
        'name',
        'surname',
    )


class VisitorListView(ListAPIView):
    """
    Точка для получения
    списка посетителей с суммой книг на руках
    """

    serializer_class = VisitorListSerializer
    queryset = Visitor.objects.filter(
        loan__return_date__isnull=True
    ).annotate(total_books_on_loan=Count('book_loaned'))
# -----------------------------------------------------------


# Department Views -------------------------------------
class DepartmentCreateView(CreateAPIView):
    """
    Точка для добавления отделов
    """

    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


class DepartmentRetrieveDestroyView(RetrieveDestroyAPIView):
    """
    Точка для получения
    и удаления отдела
    """

    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


class DepartmentListView(ListAPIView):
    """
    Точка для получения
    списка отделов
    """

    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
# -----------------------------------------------------------


# Loan And Return Book Views -------------------------------------
class LoanBookView(CreateAPIView):
    """
    Точка для оформления
    выдачи книги
    """
    queryset = Loan.objects.all()
    serializer_class = BookLoanSerializer


class ReturnBookView(UpdateAPIView):
    """
    Точка для возврата книги
    """
    queryset = Loan.objects.all()
    serializer_class = BookLoanSerializer

# -----------------------------------------------------------


# Book Views -------------------------------------

class BookFilter(FilterSet):
    available_copies_gt_zero = BooleanFilter(
        field_name='available_copies',
        method='filter_available_copies'
    )

    class Meta:
        model = Book
        fields = {
            'author': ['icontains'],
            'year_of_issue': ['exact'],
            'department__name': ['icontains'],
        }

    def filter_available_copies(self, queryset, name, value):
        if value:
            return queryset.filter(available_copies__gt=0)
        else:
            return queryset.filter(available_copies=0)


class BookListView(ListAPIView):
    """
    Точка для вывода списка книг
    с фильтрацией
    """
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# -----------------------------------------------------------
