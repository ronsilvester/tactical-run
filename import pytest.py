import pytest
from datetime import datetime
from main import Workout, Special_Goals, Goal, User

@pytest.fixture
def sample_user():
    """Fixture for creating a reusable User instance."""
    return User(name="Alice", age=30, weight=70.0, height=1.75)


@pytest.fixture
def sample_workout():
    """Fixture for creating a reusable Workout instance."""
    return Workout(date=datetime(2024, 1, 15, 10, 30), distance=10.5, rpe=7)


class TestWorkout:
    def test_workout_creation(self, sample_workout):
        assert sample_workout.distance == 10.5
        assert sample_workout.rpe == 7
        assert sample_workout.date == datetime(2024, 1, 15, 10, 30)

    def test_workout_str(self, sample_workout):
        assert "2024-01-15 10:30:00" in str(sample_workout)
        assert "10.5 km" in str(sample_workout)
        assert "RPE 7" in str(sample_workout)

    def test_invalid_rpe_below_range(self):
        with pytest.raises(ValueError, match="RPE must be an integer between 1 and 10"):
            Workout(datetime.now(), 5.0, 0)

    def test_invalid_rpe_above_range(self):
        with pytest.raises(ValueError, match="RPE must be an integer between 1 and 10"):
            Workout(datetime.now(), 5.0, 11)

    def test_invalid_distance_negative(self):
        with pytest.raises(ValueError, match="Distance must be non-negative"):
            Workout(datetime.now(), -1.0, 5)

    def test_invalid_date_type(self):
        with pytest.raises(ValueError, match="Date must be a datetime object"):
            Workout("2024-01-15", 5.0, 5)


class TestSpecialGoals:
    def test_special_goals_race_goal(self):
        goal = Special_Goals("marathon", target_time=180.0, weeks_to_target=16)
        assert goal.goal_type == "marathon"
        assert goal.target_distance == 42.2
        assert goal.target_time == 180.0
        assert goal.weeks_to_target == 16

    def test_special_goals_idf_selection(self):
        goal = Special_Goals("special_forces", weeks_to_target=12)
        assert goal.goal_type == "special_forces"
        assert goal.target_distance is None
        assert goal.weeks_to_target == 12

    def test_invalid_goal_type(self):
        with pytest.raises(ValueError, match="Invalid goal type"):
            Special_Goals("invalid_goal")


class TestGoal:
    def test_goal_special_type(self):
        goal = Goal(
            "special",
            special_goal_type="marathon",
            target_time=180.0,
            weeks_to_target=16
        )
        assert goal.description == "marathon"
        assert goal.target_distance == 42.2
        assert goal.weeks_to_target == 16

    def test_goal_special_idf_type(self):
        goal = Goal(
            "special",
            special_goal_type="special_forces",
            weeks_to_target=12
        )
        assert goal.description == "special_forces"
        assert goal.target_distance is None

    def test_goal_custom_type(self):
        goal = Goal(
            "custom",
            target_distance=21.0,
            target_time=120.0,
            weeks_to_target=8
        )
        assert goal.description == "Custom Goal"
        assert goal.target_distance == 21.0
        assert goal.target_time == 120.0

    def test_goal_custom_distance_too_low(self):
        with pytest.raises(ValueError, match="Target distance must be between 2 and 42.2 km"):
            Goal("custom", target_distance=1.0)

    def test_goal_custom_distance_too_high(self):
        with pytest.raises(ValueError, match="Target distance must be between 2 and 42.2 km"):
            Goal("custom", target_distance=50.0)

    def test_goal_invalid_type(self):
        with pytest.raises(ValueError, match="Goal type must be 'special' or 'custom'"):
            Goal("invalid")

    def test_goal_str_representation(self):
        goal = Goal("custom", target_distance=10.0, weeks_to_target=4)
        goal_str = str(goal)
        assert "Custom Goal" in goal_str
        assert "10.0 km" in goal_str


class TestUser:
    def test_user_creation(self, sample_user):
        assert sample_user.name == "Alice"
        assert sample_user.age == 30
        assert sample_user.weight == 70.0
        assert sample_user.height == 1.75
        assert sample_user.workouts == []
        assert sample_user.current_goal is None

    def test_add_single_workout(self, sample_user, sample_workout):
        sample_user.add_workout(sample_workout)
        assert len(sample_user.workouts) == 1
        assert sample_user.workouts[0] == sample_workout

    def test_add_multiple_workouts(self, sample_user):
        workout1 = Workout(datetime(2024, 1, 15, 10, 0), 5.0, 5)
        workout2 = Workout(datetime(2024, 1, 16, 10, 0), 8.0, 7)
        sample_user.add_workout(workout1)
        sample_user.add_workout(workout2)
        assert len(sample_user.workouts) == 2
        assert sample_user.workouts[0] == workout1
        assert sample_user.workouts[1] == workout2

    def test_add_invalid_workout(self, sample_user):
        with pytest.raises(ValueError, match="Expected a Workout instance"):
            sample_user.add_workout("not a workout")

    def test_set_goals(self, sample_user):
        goal = Goal("custom", target_distance=10.0, weeks_to_target=4)
        sample_user.set_goals(goal)
        assert sample_user.current_goal == goal
        assert sample_user.current_goal.target_distance == 10.0

    def test_set_special_goal(self, sample_user):
        goal = Goal("special", special_goal_type="5k", weeks_to_target=6)
        sample_user.set_goals(goal)
        assert sample_user.current_goal.target_distance == 5.0


class TestIntegration:
    def test_user_workout_integration(self, sample_user):
        workout1 = Workout(datetime(2024, 1, 15, 10, 0), 5.0, 5)
        workout2 = Workout(datetime(2024, 1, 16, 15, 30), 12.0, 8)
        sample_user.add_workout(workout1)
        sample_user.add_workout(workout2)
        assert len(sample_user.workouts) == 2
        total_distance = sum(w.distance for w in sample_user.workouts)
        assert total_distance == 17.0

    def test_user_goal_workout_integration(self, sample_user):
        goal = Goal("custom", target_distance=21.0, weeks_to_target=8)
        sample_user.set_goals(goal)
        workout = Workout(datetime(2024, 1, 15, 10, 0), 10.0, 6)
        sample_user.add_workout(workout)
        assert sample_user.current_goal.target_distance == 21.0
        assert len(sample_user.workouts) == 1

    def test_special_goals_flattening_to_goal(self):
        goal = Goal(
            "special",
            special_goal_type="half_marathon",
            target_time=105.0,
            weeks_to_target=12
        )
        assert goal.target_distance == 21.1
        assert goal.description == "half_marathon"
        assert goal.weeks_to_target == 12