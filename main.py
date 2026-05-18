from datetime import datetime
from models import User, Workout, Goal, Gender, Special_Goals
from logic import Calculator_ACWR
def main():
    user = User(
        name="Noa",
        age=25,
        weight=60.0,
        height=165.0,
        gender=Gender.FEMALE
    )

    goal = Goal(
        goal_type="special",
        special_goal_type="special_forces",
        weeks_to_target=12
    )
    user.set_goals(goal)

    workout = Workout(
        date=datetime.now(),
        distance=5.0,
        rpe=7,
        duration_min=40
    )
    user.add_workout(workout)

    print(f"--- Tactical Run Platform ---")
    print(f"User: {user.name}")
    print(f"Goal: {user.current_goal.description}")
    print(f"Workouts Logged: {len(user.workouts)}")
    print(f"Latest Activity: {user.workouts[-1]}")
    
    acwr_calculator = Calculator_ACWR(user.workouts)
    acwr_ratio = acwr_calculator.calculate()
    print(f"ACWR Ratio: {acwr_ratio}")

if __name__ == "__main__":
    main()