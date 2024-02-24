from rest_framework import serializers
from rest_framework.generics import (
    get_object_or_404,
)
from base.models import (
    Visitor,
    Department,
    Loan,
    Book
)

from django.utils import timezone


class VisitorSerializer(serializers.ModelSerializer):
    surname = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Visitor
        fields = "__all__"
        read_only_fields = ["id"]


class LoanSerializer(serializers.Serializer):
    """
    Сериализатор для вывода списка книг посетителя
    """
    book_id = serializers.IntegerField()
    book_title = serializers.CharField(source="book.title")


class VisitorRetrieveSerializer(serializers.ModelSerializer):
    books = LoanSerializer(many=True, read_only=True, source="loan_set")

    class Meta:
        model = Visitor
        fields = ['id', 'family_name', 'name', 'surname', 'books']


class VisitorListSerializer(serializers.ModelSerializer):
    total_books = serializers.IntegerField(source='total_books_on_loan')

    class Meta:
        model = Visitor
        fields = ['id', 'family_name', 'name', 'surname', 'total_books']


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = "__all__"
        read_only_fields = ["id"]


class BookLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['id', 'book', 'visitor', 'loan_date', 'return_date']

    def create(self, validated_data):
        book_id = self.context['view'].kwargs.get('book_id')
        visitor_id = self.context['view'].kwargs.get('visitor_id')

        book = get_object_or_404(Book, pk=book_id)
        visitor = get_object_or_404(Visitor, pk=visitor_id)

        if book.available_copies <= 0:
            raise serializers.ValidationError("Не осталось экземпляров данной книги")

        loan = Loan.objects.create(book=book, visitor=visitor)
        book.available_copies -= 1
        book.save()

        return loan

    def update(self, instance, validated_data):
        if instance.return_date:
            raise serializers.ValidationError("Книга уже возвращена")

        instance.return_date = timezone.now()
        instance.book.available_copies += 1
        instance.book.save()
        instance.save()

        return instance


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ["id"]


