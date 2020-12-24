from django.db import models

# Create your models here.


class IDC(models.Model):
    id = models.AutoField(primary_key=True)
    vendors = models.CharField(max_length=32)
    system = models.CharField(max_length=32)
    region = models.CharField(max_length=32)
    ip = models.CharField(max_length=32)
    status = models.CharField(max_length=32)
    configuration = models.CharField(max_length=64)

    class Meta:
        db_table = "IDC"


class APPLICATION(models.Model):
    application = models.CharField(max_length=128)
    env = models.ForeignKey(to='ENV', on_delete=models.CASCADE)
    idc = models.ManyToManyField(to='IDC', related_name='APPLICATION')

    class Meta:
        db_table = "APPLICATION"


class DOMAIN(models.Model):
    domain = models.CharField(max_length=128)
    application = models.ForeignKey(to='APPLICATION', on_delete=models.CASCADE)

    class Meta:
        db_table = "DOMAIN"


class ENV(models.Model):
    env = models.CharField(max_length=32)
    lanuage = models.ForeignKey(to='LANUAGE', on_delete=models.CASCADE)

    class Meta:
        db_table = "ENV"


class LANUAGE(models.Model):
    lanuage = models.CharField(max_length=32)

    class Meta:
        db_table = "LANUAGE"


