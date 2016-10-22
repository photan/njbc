class Person(models.Model):
    sname             = models.CharField(max_length=64)
    email             = models.CharField(max_length=128,blank=True)
    phone             = models.CharField(max_length=32,blank=True)
    first_name        = models.CharField(max_length=64)
    last_name         = models.CharField(max_length=64)
    usba_id           = models.CharField(max_length=32,blank=True)
    njbc_id           = models.CharField(max_length=32,blank=True)
    njbc_expiry_date  = models.DateTimeField(blank=True, null=True)
    njbc_since        = models.DateTimeField(blank=True, null=True)
    note              = models.CharField(max_length=128,blank=True)
    emergency_contact = models.CharField(max_length=128,blank=True)
    emergency_email   = models.CharField(max_length=128,blank=True)
    emergency_phone   = models.CharField(max_length=32,blank=True)
    def __str__(self):
        return self.sname

    def get_absolute_url(self):
        return reverse('person_detail', args=[str(self.id)])    

    class Meta:
       ordering = ['-sname']    