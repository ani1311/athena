import re
from src.database.db import GoalTransactor
from src.database.models import Goal


class AgentDBTools:
    def __init__(self, db):
        self.db = db
        self.goal_transactor = GoalTransactor(db.get_session())

    def get_goals(self) -> str:
        """
        Retrieves all active goals from the database.

        Returns:
            str: A formatted string representation of all active goals.
        """
        goals = self.goal_transactor.get_active_goals()
        if not goals:
            return "No active goals found."

        goal_list = []
        for goal in goals:
            goal_list.append(
                f"ID: {goal.id}, Description: {goal.description}, Created: {goal.created_at}"
            )

        return "\n".join(goal_list)

    def add_goal(self, description: str) -> str:
        """
        Creates a new goal with the given description.

        Args:
            description (str): The description of the goal to be added.
        Returns:
            str: A confirmation message with the created goal's details.
        """
        goal = self.goal_transactor.add_goal(description)
        return (
            f"Goal created successfully! ID: {goal.id}, Description: {goal.description}"
        )

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
