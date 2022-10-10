from typing import Any, Dict

from users.models import Group


class GroupService:
    non_side_effect_fields = ['name', 'permissions']

    def group_create(self, data: Dict[str, Any]) -> Group:
        return Group.model_create(
            fields=self.non_side_effect_fields,
            data=data,
        )

    def group_update(self, group: Group, data: Dict[str, Any]) -> Group:
        group, _ = group.model_update(
            fields=self.non_side_effect_fields,
            data=data,
        )
        return group
