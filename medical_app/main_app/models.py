from django.db import models

# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
#
# User = get_user_model()
#
#
# class Doctor(models.Model):
#     """User model who have a valid medical license and can change data at the DB. """
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     medical_license = models.CharField(max_length=255)
#
#
# class Patient(models.Model):
#     """User model who don't have a valid medical license and can only view data from the DB. """
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


class Organ(models.Model):
    """ Human organs model. """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(default=True, upload_to='media/organs/')

    def __str__(self):
        return self.name


class Symptom(models.Model):
    """ Symptoms model. """

    name = models.CharField(max_length=255)
    affected_organ = models.ForeignKey(Organ, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class GeographicalArea(models.Model):
    """ Geographical Area model. """

    area = models.TextField()
    image = models.ImageField(default=True, upload_to='media/geographical_area/')

    def __str__(self):
        return self.area


class Treatment(models.Model):
    """ Treatment model. """

    treatment = models.TextField()

    def __str__(self):
        return self.treatment


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
    symptom_frequency = models.PositiveSmallIntegerField(choices=SYMPTOM_FREQUENCY_CHOICES, default=0)

    def __str__(self):
        return f'{self.disease} / {self.symptom}'
