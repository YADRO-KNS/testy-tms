
from django.db.models import QuerySet
from users.models import Group


class GroupSelector:
    def group_list(self) -> QuerySet[Group]:
        return Group.objects.all()
