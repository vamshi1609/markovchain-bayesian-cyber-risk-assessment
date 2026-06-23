from django.db import models


class Asset(models.Model):
    name = models.CharField(max_length=200)
    criticality = models.FloatField(default=1.0)

    def __str__(self):
        return self.name


class Vulnerability(models.Model):
    cve = models.CharField(max_length=20, unique=True)
    epss_score = models.FloatField(null=True, blank=True)
    assets = models.ManyToManyField(Asset, through='AssetVulnerability')

    def __str__(self):
        return self.cve


class AssetVulnerability(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    vuln = models.ForeignKey(Vulnerability, on_delete=models.CASCADE)
    probability = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('asset', 'vuln')


class AssetDependency(models.Model):
    source = models.ForeignKey(
        Asset,
        related_name='dependents',
        on_delete=models.CASCADE,
    )
    target = models.ForeignKey(
        Asset,
        related_name='dependencies',
        on_delete=models.CASCADE,
    )
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.source} -> {self.target}"