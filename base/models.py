from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year_of_issue = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)


class Visitor(models.Model):
    family_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, null=True, blank=True)
    book_loaned = models.ManyToManyField(
        Book,
        through='Loan',
    )

    def __str__(self):
        return f"{self.family_name} {self.name} {self.surname}"


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.visitor.name} borrowed {self.book.title}"