from typing import Any, Dict

from users.models import Group


class GroupService:
    non_side_effect_fields = ['name']

    def group_create(self, data: Dict[str, Any]) -> Group:
        group = Group.model_create(
            fields=self.non_side_effect_fields,
            data=data,
            commit=False
        )
        group.full_clean()
        group.save()
        group.permissions.set(data.get('permissions', []))
        group.full_clean()
        group.save()
        return group

    def group_update(self, group: Group, data: Dict[str, Any]) -> Group:
        group, _ = group.model_update(
            fields=self.non_side_effect_fields,
            data=data,
            commit=False
        )
        group.permissions.set(data.get('permissions', []))
        group.full_clean()
        group.save()
        return group
