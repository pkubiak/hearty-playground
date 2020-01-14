from django.db import models
from course_app.models import Activity  #, ActivityContent


class ActivityQuiz(Activity):
    """TODO: """

    fa_icon = "fas fa-tasks"

    text = models.TextField(null=False, blank=False)

    # completable = models.BooleanField(null=False, default=False, choices=((True, 'YES'), (False, 'NO')))
    @property
    def completable(self):
        return True
