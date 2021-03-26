from django.db import models

# Create your models here.

class UserType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.type}'

class User(models.Model):
    fname=models.CharField(max_length=50)
    lname =models.CharField(max_length=50,null=True)
    gen = models.CharField(max_length=7)
    email = models.EmailField(max_length=100,unique=True)
    pwd = models.CharField(max_length=10)
    utype = models.ForeignKey(UserType,on_delete=models.CASCADE)
    approvedby = models.IntegerField(null=True)
    approveldt = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.id}--{self.fname}--{self.lname}--{self.gen}--{self.email}--{self.utype}--{self.approvedby}--{self.approveldt}'


class Logindetail(models.Model):
    users=models.ForeignKey(User,on_delete=models.CASCADE)
    logindt=models.DateTimeField()

    def __str__(self):
        return f'{self.users}-{self.logindt}'

class Ticket_type(models.Model):
    tctype = models.CharField(max_length=70)
    def __str__(self):
        return f'{self.tctype}'

class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.category}'


class Ticket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=100,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    ticket_type =models.ForeignKey(Ticket_type,on_delete=models.CASCADE)
    question = models.CharField(max_length=250)
    desc =models.TextField(null=True)
    trd = models.DateTimeField(null=True)
    tod = models.DateTimeField(null=True)
    tcd = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.id}--{self.user}--{self.status}--{self.category}--{self.ticket_type}-{self.question}--{self.desc}--{self.trd}'