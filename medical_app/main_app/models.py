from django.db import models


class Organ(models.Model):
    ''' Human organs model. '''

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Symptom(models.Model):
    ''' Symptoms model. '''

    name = models.CharField(max_length=255)
    affected_organ = models.ForeignKey(Organ, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Disease(models.Model):
    ''' Disease model. '''

    name = models.CharField(max_length=255)
    description = models.TextField()
    symptoms = models.ManyToManyField(Symptom, through='DiseaseSymptom')
    affected_organs = models.ManyToManyField(Organ)
    geographical_area = models.TextField()
    treatment = models.TextField()

    def __str__(self):
        return self.name


class DiseaseSymptom(models.Model):
    ''' Disease symptom frequency model. Related with Disease model. '''

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


class User(models.Model):
    ''' User model. '''

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

