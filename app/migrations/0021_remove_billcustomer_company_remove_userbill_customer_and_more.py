# Generated by Django 5.0.3 on 2024-05-11 14:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0020_rename_name_billcustomer_bill_number"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="billcustomer",
            name="company",
        ),
        migrations.RemoveField(
            model_name="userbill",
            name="customer",
        ),
        migrations.RemoveField(
            model_name="userbill",
            name="user",
        ),
        migrations.DeleteModel(
            name="BillCompany",
        ),
        migrations.DeleteModel(
            name="BillCustomer",
        ),
        migrations.DeleteModel(
            name="UserBill",
        ),
    ]