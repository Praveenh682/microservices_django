from django.db import models

class ProductMaster(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=100,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.IntegerField()
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_master'
        ordering = ('created_at',)

class VariantMaster(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=100,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.IntegerField()
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'variant_master'
        ordering = ('created_at',)


class VariantOption(models.Model):
    variant = models.ForeignKey(VariantMaster,on_delete=models.CASCADE,null=True,related_name='variant_master_name')
    name = models.CharField(max_length=100,null=True,blank=True)
    description = models.CharField(max_length=100,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.IntegerField()
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'variant_option'
        ordering = ('created_at',)

class ProductOverallQuantity(models.Model):
    product = models.ForeignKey(ProductMaster,on_delete=models.CASCADE,related_name='product_master_name')
    variant_option = models.ForeignKey(VariantOption,on_delete=models.CASCADE,related_name='variant_option_product_name')
    is_active = models.BooleanField(default=True)
    created_by = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.IntegerField()
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_overall_quantity'
        ordering = ('created_at',)
