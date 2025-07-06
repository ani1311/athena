import re
from src.database.db import GoalTransactor
from src.database.models import Goal


class AgentDBTools:
    def __init__(self, db):
        self.db = db
        self.goal_transactor = GoalTransactor(db.get_session())

    def get_goals(self):
        """
        Retrieves all active goals from the database.

        Returns:
            List[Goal]: A list of active Goal objects.
        """
        return self.goal_transactor.get_active_goals()

    def add_goal(self, description):
        """
        creates a new goal with the given description.

        Args:
            description (str): The description of the goal to be added.
        Returns:
            Goal: The newly created goal object.
        """
        return self.goal_transactor.add_goal(description)

    def get_todays_tasks(self):
        return self.db.get_todays_tasks()

    def get_all_tasks(self):
        return self.db.get_all_tasks()

    def get_task_by_id(self, task_id):
        return self.db.get_task_by_id(task_id)

    def add_task(self, task):
        return self.db.add_task(task)

    def update_task(self, task):
        return self.db.update_task(task)

    def delete_task(self, task_id):
        return self.db.delete_task(task_id)
