from typing import Any, Dict

from core.models import Project


class ProjectService:
    non_side_effect_fields = ['name', 'description', 'is_archive']

    def project_create(self, data: Dict[str, Any]) -> Project:
        return Project.model_create(
            fields=self.non_side_effect_fields,
            data=data,
        )

    def project_update(self, project: Project, data: Dict[str, Any]) -> Project:
        project, _ = project.model_update(
            fields=self.non_side_effect_fields,
            data=data,
        )
        return project
