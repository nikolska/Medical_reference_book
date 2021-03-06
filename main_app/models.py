from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class GeographicalArea(models.Model):
    """ Geographical Area model. """

    area = models.TextField()
    image = models.ImageField(upload_to='geographical_area/')

    def __str__(self):
        return self.area

    class Meta:
        ordering = ['area']


class Organ(models.Model):
    """ Human organs model. """

    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='organs/')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Symptom(models.Model):
    """ Symptoms model. """

    name = models.CharField(max_length=255)
    affected_organ = models.ForeignKey(Organ, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Treatment(models.Model):
    """ Treatment model. """

    treatment = models.TextField()

    def __str__(self):
        return self.treatment

    class Meta:
        ordering = ['treatment']


class Disease(models.Model):
    """ Disease model. """

    name = models.CharField(max_length=255)
    description = models.TextField()
    symptoms = models.ManyToManyField(Symptom, through='DiseaseSymptom')
    affected_organs = models.ManyToManyField(Organ)
    geographical_area = models.ManyToManyField(GeographicalArea)
    treatment = models.ManyToManyField(Treatment)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Get URl to the singe object of the model."""
        return reverse('disease_details', args=[str(self.pk)])

    class Meta:
        ordering = ['name']


class DiseaseSymptom(models.Model):
    """ Disease symptom frequency model. Related with Disease model. """

    SYMPTOM_FREQUENCY_CHOICES = (
        (0, 'not chosen'),
        (1, 'very rarely'),
        (2, 'rarely'),
        (3, 'sometimes'),
        (4, 'often'),
        (5, 'constantly')
    )

    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    symptom_frequency = models.PositiveSmallIntegerField(
        choices=SYMPTOM_FREQUENCY_CHOICES, 
        default=0
    )

    def __str__(self):
        return f'{self.disease} / {self.symptom}'

    class Meta:
        ordering = ['disease']


class User(AbstractUser):
    """User model."""
    medical_license = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    @property
    def full_name(self):
        """Return user first name and last name."""
        return f'{self.first_name} {self.last_name}'
