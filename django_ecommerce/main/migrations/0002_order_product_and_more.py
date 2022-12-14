# Generated by Django 4.1.2 on 2022-12-07 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('is_delivered', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=100)),
                ('product_desc', models.CharField(max_length=1000)),
                ('product_price', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='customer_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='customer_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='customer_mobile',
            new_name='mobile',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='customer_name',
            new_name='name',
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('product_image_id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.CharField(max_length=2000)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('order_details_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_price', models.IntegerField()),
                ('product_quantity', models.IntegerField()),
                ('subtotal', models.IntegerField()),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.order')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.customer'),
        ),
    ]
