from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver


class TeamMember(models.Model):
	image = models.ImageField(_('Изображение'), upload_to='team/')
	username = models.CharField('@username', max_length=32)
	speciality = models.CharField(_('Специальность'), max_length=255)
	joined_date = models.DateTimeField(_('Присоединился'))

	class Meta:
		db_table = 'team_member'
		ordering = ['joined_date']

		verbose_name = _('Члена')
		verbose_name_plural = _('Члены')

	def __str__(self) -> str:
		return f'@{self.username}'

@receiver(post_delete, sender=TeamMember)
def post_delete_team_member_signal(instance: TeamMember, **kwargs) -> None:
	instance.image.delete(save=False)
