from django.db import models


class PM(models.Model):
    pm_name = models.CharField(max_length=100, verbose_name="Proxmox nodename")
    pm_ip_address = models.CharField(max_length=100, verbose_name="Proxmox ip address", blank=True, null=True)
    pm_token = models.CharField(max_length=255, verbose_name="Proxmox token", blank=True, null=True)

    def __str__(self):
        return self.pm_name

    class Meta:
        ordering = ("id",)
        verbose_name = "Proxmox node"
        verbose_name_plural = "Proxmox nodes"