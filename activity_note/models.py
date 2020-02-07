from django.db import models
from course_app.models import Activity, Solution


class ActivityNote(Activity):
    """TODO: """

    fa_icon = "fas fa-book"

    text = models.TextField(null=False, blank=True)

    completable = models.BooleanField(null=False, default=False, choices=((True, 'YES'), (False, 'NO')))

    def is_completed(self, user):
        try:
            solution = SolutionNote.objects.get(activity_id=self.id, user_id=user.id)
            return solution.completed
        except models.DoesNotExists:
            return False


class SolutionNote(Solution):
    pass
