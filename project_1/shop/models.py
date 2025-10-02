from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Category Name')
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Product Name')
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='Discount')
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock Quantity')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    class Meta:
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='products/', verbose_name='Image File')

    class Meta:
        db_table = 'product_image'
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
