from django.db import models
from course_app.models import Activity  #, ActivityContent


class ActivityNote(Activity):
    """TODO: """

    fa_icon = "fas fa-book"

    text = models.TextField(null=False, blank=True)

    completable = models.BooleanField(null=False, default=False, choices=((True, 'YES'), (False, 'NO')))
