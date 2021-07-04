from django.db import models
import shortuuid


class Customer(models.Model):
    """A model of a Customer."""
    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150)
    email = models.EmailField('email address', unique=True)

    def __str__(self):
        return self.email


class Offer(models.Model):
    """A model of a Offer."""
    name = models.CharField(unique=True, max_length=256)
    discount = models.IntegerField()

    def __str__(self):
        return self.name


def short_uuid4():
    uuid = shortuuid.ShortUUID(alphabet="23456789ABCDEFGHJKLMNPQRSTUVWXYZ")
    return uuid.random(length=8)

class Voucher(models.Model):
    """A model of a Voucher."""
    code = models.CharField(unique=True, default=short_uuid4 , editable=False, max_length=256)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    expiration = models.DateField()
    used_on = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.code

