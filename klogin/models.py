from django.db import models

# Create your models here.
class infostock(models.Model):
    stock_code = models.CharField(max_length=10)
    date = models.CharField(max_length=10)
    open = models.IntegerField()
    high = models.IntegerField()
    low = models.IntegerField()
    close = models.IntegerField()
    volume = models.IntegerField()

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}, {}".format(self.stock_code, self.date, str(self.open), str(self.high),str(self.low),str(self.close),str(self.volume))

class scode(models.Model):
    stock_code = models.CharField(max_length=30)
    stock_name = models.CharField(max_length=10)

    def __str__(self):
        return "{} {}".format(self.stock_code, self.stock_name)

class predicted_by_ts(models.Model):
    stock_code = models.CharField(max_length=10)
    date = models.CharField(max_length=10)
    stock_price = models.CharField(max_length=30)

    def __str__(self):
        return "{} {} {}".format(self.stock_code, self.date, self.stock_price)

class favorite(models.Model):
    uid = models.CharField(max_length=50)
    stock_code = models.CharField(max_length=10)

    def __str__(self):
        return "{} {}".format(self.uid, self.stock_code)

class Note(models.Model):
    uid = models.CharField(max_length=50)
    text = models.CharField(max_length=3000)

    def __str__(self):
        return "{} {}".format(self.uid, self.text)