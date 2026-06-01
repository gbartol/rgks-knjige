# RGKS Projekt

## Upute

### Instalacija
- Backend
```
cd backend
python -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install
```
- Frontend
```
cd frontend
npm install
```
### Napomene
- Napravi admin account da možeš vidjeti django admin stranicu:
```
cd backend
python manage.py createsuperuser
```
- Kad napravimo model moramo ga registrirati za admin stranicu u backend/api/admin.py, npr. ako smo napravili model Task moramo staviti:
```
from .models import Task


admin.site.register(Task)
```
- Kad napravimo novu rutu moramo je staviti u backend/api/urls.py, npr. ovako:
```
from django.urls import path

from . import views


urlpatterns = [
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/<int:pk>/', views.task_detail, name='task-detail'),
]
```
- Stavio sam paginaciju u backend/config/settings.py i page size na 20 (kod "REST_FRAMEWORK = ...")
- ... i tu sam stao, kod vue-query dijela. Ako se sjetim još nečega napišem.
