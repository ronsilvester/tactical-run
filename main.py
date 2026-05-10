from datetime import datetime

class Workout:
    def __init__(self, date: datetime, distance: float, rpe: int):
        if not isinstance(date, datetime):
            raise ValueError("Date must be a datetime object")
        if not (1 <= rpe <= 10):
            raise ValueError("RPE must be an integer between 1 and 10")
        if distance < 0:
            raise ValueError("Distance must be non-negative")
        
        self.date = date
        self.distance = distance
        self.rpe = rpe

    def __str__(self):
        return f"Workout on {self.date.strftime('%Y-%m-%d %H:%M:%S')}: {self.distance} km, RPE {self.rpe}"
    
   
          
            
    class Special_Goals:
        RACE_GOALS = {
            "marathon": 42.2,
            "half_marathon": 21.1,
            "10k": 10.0,
            "5k": 5.0
        }
        
        IDF_SELECTIONS = {
            "special_forces": "Special Forces Selection Day",
            "combat_instructor": "Combat Fitness Instructor Selection",
            "female_combat": "Female Combat Units Selection",
            "pft": "Combat Fitness Assessment - PFT",
            "gibush": "Unit Specific Selection Gibush",
            "officer": "Officer Selection Test"
        }
        
        def __init__(self, goal_type: str, target_time: float = None, weeks_to_target: int = None):
            self.goal_type = goal_type
            self.target_time = target_time
            self.weeks_to_target = weeks_to_target
            
            if goal_type in self.RACE_GOALS:
                self.target_distance = self.RACE_GOALS[goal_type]
            elif goal_type in self.IDF_SELECTIONS:
                self.target_distance = None
            else:
                raise ValueError(f"Invalid goal type: {goal_type}")
        
        class Goal:
            def __init__(self, goal_type: str, **kwargs):
                if goal_type == "special":
                    self.goal = Special_Goals(
                        kwargs.get("special_goal_type"),
                        kwargs.get("target_time"),
                        kwargs.get("weeks_to_target")
                    )
                    self.target_distance= self.goal.target_distance
                    self.description = self.goal.goal_type
                elif goal_type == "custom":
                    target_distance = kwargs.get("target_distance")
                    if not (2 <= target_distance <= 42.2):
                        raise ValueError("Target distance must be between 2 and 42.2 km")
                    self.target_distance = target_distance
                    self.target_time = kwargs.get("target_time")
                    self.weeks_to_target = kwargs.get("weeks_to_target")
                    self.description = "Custom Goal"
                else:
                    raise ValueError("Goal type must be 'special' or 'custom'")
            def __str__(self):
                 dist_str = f"{self.target_distance} km" if self.target_distance else "N/A"
                 return f"Goal: {self.description} | Distance: {dist_str} | Target: {self.weeks_to_target} weeks"
              