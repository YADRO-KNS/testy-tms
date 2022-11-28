# TestY TMS - Test Management System
# Copyright (C) 2022 KNS Group LLC (YADRO)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.
#
# If your software can interact with users remotely through a computer
# network, you should also make sure that it provides a way for users to
# get its source.  For example, if your program is a web application, its
# interface could display a "Source" link that leads users to an archive
# of the code.  There are many ways you could offer source, and different
# solutions will be better for different programs; see section 13 for the
# specific requirements.
#
# You should also get your employer (if you work as a programmer) or school,
# if any, to sign a "copyright disclaimer" for the program, if necessary.
# For more information on this, and how to apply and follow the GNU AGPL, see
# <http://www.gnu.org/licenses/>.
import mimetypes
import os

from core.models import Project
from django.conf import settings
from django.contrib.admin.utils import unquote
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.views.generic import DetailView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from views import Tab


class ProjectBaseView:
    model = Project
    active_tab = 'project_details'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super(ProjectBaseView, self).get_context_data(**kwargs)
        context['tabs'] = [Tab('Overview', 'project_details', self.kwargs['pk']),
                           Tab('Test Suites & Cases', 'project_suites', self.kwargs['pk']),
                           Tab('Test Plans & Results', 'project_runs', self.kwargs['pk'])]
        context['active_tab'] = self.active_tab
        return context


class ProjectOverviewView(ProjectBaseView, DetailView):
    model = Project
    template_name = 'testy/project/overview.html'


class ProjectPlansView(ProjectBaseView, DetailView):
    model = Project
    template_name = 'testy/project/test_runs.html'
    active_tab = 'project_runs'


class ProjectSuitesView(ProjectBaseView, DetailView):
    model = Project
    template_name = 'testy/project/test_suites.html'
    active_tab = 'project_suites'


class MediaView(APIView):

    def get(self, request, path):
        if not os.path.exists(f"{settings.MEDIA_ROOT}/{path}"):
            return Response("No such file exists.", status=status.HTTP_404_NOT_FOUND)
        mimetype, encoding = mimetypes.guess_type(path, strict=True)
        if not mimetype:
            mimetype = "text/html"
        file_path = unquote(os.path.join(settings.MEDIA_ROOT, path)).encode("utf-8")
        return FileResponse(open(file_path, "rb"), content_type=mimetype)
