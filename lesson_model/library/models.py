from django.db import models
import random
import datetime
from django.utils import timezone
from django.db.models import Count
from django.db.models import Q


# Create your models here.


class Profile(models.Model):
    slug = models.SlugField()
    username = models.CharField(unique=True, max_length=60)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.IntegerField(unique=True)
    address = models.TextField()

    def random_data(self):
        random_names = ['Tom', 'Nick', 'John', 'Yoda', 'Shivansh', 'Akash', 'Akbar']
        streets=['Baner','CP','Ifco chowk']
        cities=['NYC','Delhi','Pune','Mumbai']
        my_list = []
        for i in range(50000):
            usernames = f'{random.choice(random_names)}{i}'
            slugs = f'{usernames}{i}'
            emails = f'{usernames}{i}@lib.com'
            phones= random.randint(1000000000, 9999999999)
            addresss = f'{random.randint(1, 1000)} {random.choice(streets)} Street, {random.choice(cities)} City '
            obj = Profile(slug=slugs, username=usernames,email=emails,phone=phones,address=addresss)

            my_list.append(obj)

        Profile.objects.bulk_create(my_list)


class Author(models.Model):
    slug=models.SlugField()
    name=models.CharField(max_length=60,unique=True)
    profile=models.OneToOneField(Profile,on_delete=models.CASCADE)
    
    def author_random_data(self):
        my_list=[]
        p = list(Profile.objects.all())
        random_names = ['Tom', 'Nick', 'John', 'Yoda', 'Shivansh', 'Akash', 'Akbar']
        for i in range(50000):
            names = f'{random.choice(random_names)}{i}'
            slugs = f'{names}{i}'
            obj = Author(slug=slugs, name=names,profile=p[i])

            my_list.append(obj)

        Author.objects.bulk_create(my_list)

    def author_list(self):
        profiles =Author.objects.all()
        answer=[profile.name for profile in profiles]
        return answer
    
    def get_author_with_profile_detail(self):
        return Author.objects.select_related('profile').values('name', 'profile__username', 'profile__email', 'profile__phone', 'profile__address')

    @classmethod
    def authors_with_more_than_two_books(cls):
        return cls.objects.annotate(num_books=Count('book')).filter(num_books__gt=2).values('name')
    

    @classmethod
    def get_profile_by_author_name(cls, author_name):
        return Profile.objects.filter(author__name__iexact=author_name).values('username', 'email', 'phone', 'address')

    @classmethod
    def get_books_count_by_author(cls):
        return cls.objects.annotate(num_books=Count('book')).values('name', 'num_books')



class Publisher(models.Model):
    slug=models.SlugField()
    name = models.CharField(max_length=50, unique=True)
    website=models.URLField()
    email=models.EmailField()
    address=models.TextField()

    def publisher_random_data(self):
        random_names = ['Shivansh', 'Akbar', 'Kunal', 'Reacher']
        website_names=['TMC','Ncert','Rd Sharma']
        cities=['NYC','Delhi','Pune','Mumbai']
        streets=['Baner','CP','Ifco chowk']
        my_list = []
        for i in range(50000):
            names = f'{random.choice(random_names)}{i}'
            slugs = f'{names}{i}'
            websites= f'{random.choice(website_names)}{i}@book.com'
            emails = f'{names}{i}@lib.com'
            
            addresss = f'{random.randint(1, 1000)} {random.choice(streets)} Street, {random.choice(cities)} City '
            obj = Publisher(slug=slugs, name=names,email=emails,website=websites,address=addresss)
            my_list.append(obj)

        Publisher.objects.bulk_create(my_list)


class Book(models.Model):
    slug=models.SlugField()
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    title=models.CharField(max_length=30)
    publisher=models.ForeignKey(Publisher,on_delete=models.CASCADE)
    date_of_pub=models.DateField()
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_of_pub']

    def publisher_random_data(self):
        random_titles = ['Alchemy', 'Nature', 'Gandhi', 'PM']
        auth=list(Author.objects.all())
        p = list(Publisher.objects.all())
        my_list = []
        for i in range(50000):
            titles = f'{random.choice(random_titles)}{i}'
            slugs = f'{titles}{i}'
            date_of_pubs = timezone.now() - timezone.timedelta(days=random.randint(1, 36500))
            
            obj = Book(slug=slugs, title=titles ,date_of_pub=date_of_pubs,author=auth[i],publisher=p[i])
            my_list.append(obj)

        Book.objects.bulk_create(my_list)
        
    @classmethod
    def books_by_authors_starting_with_a(cls):
        return cls.objects.filter(author__name__istartswith='a').values('title', 'author__name')
    
    
    @classmethod
    def books_by_author_name(cls, author_name):
        return cls.objects.filter(author__name__iexact=author_name).values('title', 'author__name')

    @classmethod
    def books_by_author_and_publisher(cls, author_name, publisher_name):
        return cls.objects.filter(author__name__iexact=author_name, publisher__name__iexact=publisher_name).values('title', 'author__name', 'publisher__name')
    
    @classmethod
    def books_by_author_name_ending_with_a(cls):
        return cls.objects.filter(author__name__iendswith='a').values('title', 'author__name')
    
    @classmethod
    def get_or_create_book(cls, author, title, publisher, date_of_pub):
        book, created = cls.objects.get_or_create(author=author, title=title, publisher=publisher, date_of_pub=date_of_pub)
        return {'book': book, 'created': created}
    
    @classmethod
    def books_published_in_year(cls, year):
        return cls.objects.filter(date_of_pub__year=year).values('title', 'date_of_pub')
    
    @classmethod
    def books_by_publisher_name(cls, publisher_name):
        return cls.objects.filter(publisher__name__iexact=publisher_name).values('title', 'publisher__name')


    @classmethod
    def books_by_publisher_name(cls, publisher_name):
        return cls.objects.filter(publisher__name__iexact=publisher_name).values('title', 'author__name', 'date_of_pub')

    @classmethod
    def books_by_publisher_website(cls, publisher_website):
        return cls.objects.filter(publisher__website__iexact=publisher_website).values('title', 'author__name', 'date_of_pub')

    @classmethod
    def books_by_publishers(cls, publisher_names):
        return cls.objects.filter(publisher__name__in=publisher_names).values('title', 'author__name', 'date_of_pub')

    @classmethod
    def books_by_authors_A_and_B(cls, author_name_A, author_name_B):
        return cls.objects.filter(Q(author__name__iexact=author_name_A) | Q(author__name__iexact=author_name_B)).values('title', 'author__name', 'date_of_pub')

    @classmethod
    def books_excluding_author(cls, excluded_author_name):
        return cls.objects.exclude(author__name__iexact=excluded_author_name).values('title', 'author__name', 'date_of_pub')

    
    @classmethod
    def delete_book(cls, book_id):
        try:
            book = cls.objects.get(pk=book_id)
            book.delete()
            return {'status': 'Book deleted successfully'}
        except cls.DoesNotExist:
            return {'status': 'Book does not exist'}

    @classmethod
    def soft_delete_book(cls, book_id):
        try:
            book = cls.objects.get(pk=book_id)
            book.is_deleted = True
            book.save()
            return {'status': 'Book soft deleted successfully'}
        except cls.DoesNotExist:
            return {'status': 'Book does not exist'}    


class Collection(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=30)
    book = models.ManyToManyField(Book)

    @classmethod
    def collections_random_data(cls):
        random_names = ['Shivansh', 'Akbar', 'Kunal', 'Reacher']
        my_list = []

        for i in range(50000):
            names = f'{random.choice(random_names)}{i}'
            slugs = f'{names}{i}'

            obj = cls(slug=slugs, name=names)
            obj.save()
            obj.book.add(random.choice(Book.objects.all()))
            my_list.append(obj)

        Collection.objects.bulk_create(my_list)



