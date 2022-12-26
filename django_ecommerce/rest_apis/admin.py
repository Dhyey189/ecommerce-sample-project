from django.contrib import admin
from django.utils.html import format_html
from . import models
# Register your models here.

class ProductPriceFilter(admin.SimpleListFilter):
    title = 'Price Filter'
    parameter_name = 'product_price'

    def lookups(self, request, model_admin):

        qs = model_admin.get_queryset(request)
        if qs.filter(product_price__lte = 10000).exists():
            yield ('A','less than or equal to 10000')
        if qs.filter(product_price__lte = 50000,product_price__gt = 10000).exists():
            yield ('B','between 10001 and 50000')
        if qs.filter(product_price__gt = 50000).exists():
            yield ('C','greater than 50000')

    def queryset(self, request, queryset):
        print(self.value())
        if self.value() == 'A':
            return queryset.filter(product_price__lte = 10000)
        elif self.value() == 'B':
            return queryset.filter(product_price__lte = 50000,product_price__gt = 10000)
        elif self.value() == 'C':
            return queryset.filter(product_price__gt = 50000)


# Inherits admins ModelsAdmin class so that we can customize the admin panel UI related to particular model
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    '''
    Django Admin:- https://docs.djangoproject.com/en/3.1/intro/tutorial07/
    =>custom fields to be displayed in our models
    fields = []
    fieldsets = [(),()]

    =>It will display list of obj with fields on main model page so we dont have to go in particular model
    list_display = ('','','')

    =>It will put links of that obj on the fields
    list_display_links = ('','')

    =>Filtering the data
    list_filter = ('product_price')


    '''
    fields = ['product_name','product_desc','product_price']

    list_display = ('product_name','truncate_desc','view_product')
    list_filter = (ProductPriceFilter,)
    def truncate_desc(self,obj):
        return obj.product_desc[:10]+"..."

    def view_product(self,obj):
        return format_html(f'<button ><a href=http://127.0.0.1:8000/admin/rest_apis/product/{obj.product_id}/change/ target="_blank">view</a></button>')



class OrderDetailsInline(admin.TabularInline):
    model = models.OrderDetails
    # raw_id_fields = ('product_id',)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ OrderDetailsInline,]

# admin.site.register(models.Customer)
# admin.site.register(models.Order)
admin.site.register(models.OrderDetails)
# admin.site.register(models.Product)
admin.site.register(models.ProductImage)

# inlines, custom list filter, 