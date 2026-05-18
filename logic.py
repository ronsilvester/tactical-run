from datetime import timedelta
from models import Workout

class Calculator_ACWR:
    def __init__(self, workouts):
        if not isinstance(workouts, list):
            raise ValueError("Workouts must be provided as a list")
        if any(not isinstance(w, Workout) for w in workouts):
            raise ValueError("All items must be Workout instances")
        self.workouts = sorted(workouts, key=lambda workout: workout.date)

    def calculate(self):
        if not self.workouts:
            return "No workouts available to calculate ACWR."

        latest_date = self.workouts[-1].date
        earliest_date = self.workouts[0].date

        if latest_date - earliest_date < timedelta(days=28):
            return "Not enough history: need at least 28 days of workout data."

        chronic_cutoff = latest_date - timedelta(days=28)
        acute_cutoff = latest_date - timedelta(days=7)

        acute_workload = sum(
            workout.workload() for workout in self.workouts
            if workout.date > acute_cutoff
        )
        chronic_workload = sum(
            workout.workload() for workout in self.workouts
            if workout.date > chronic_cutoff
        )

        acute_load = acute_workload / 7
        chronic_load = chronic_workload / 28

        if chronic_load == 0:
            return "Chronic load is zero; cannot compute ACWR."

        return acute_load / chronic_load