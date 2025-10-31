import psycopg2
import os
import json

class DatabaseAgent:
    def __init__(self, model_name: str, task: dict[str, str]):
        """Initialize the database agent.

        Args:
            model_name: Name of the LLM model to use
            task: a dictionary containing the user request, the directory of the files containing column meanings and business logic.
        """
        self.model_name = model_name
        self.task = task

        # Connect to the labor_certification database
        self.conn = psycopg2.connect(
            dbname="labor_certification",
            user=os.getenv("USER"),
            host="localhost",
            port="5432"
        )

    def handle_request(self) -> dict[str, str]:
        """Handle a user request and generate SQL query.

        Returns:
            Dictionary with action, SQL query, and elapsed time
        """
        pass


def main():
    """Test your DatabaseAgent class."""
    # Read task from example_task_1.json
    with open('example_task_1.json', 'r') as f:
        task = json.load(f)

    print(f"Loaded task from example_task_1.json:")
    print(f"  Request: {task['request']}")
    print(f"  Database: {task['database']}")
    print(f"  Column Meaning: {task['column_meaning']}")
    print(f"  Knowledge Base: {task['knowledge_base']}")
    print()

    agent = DatabaseAgent(model_name="gpt-4", task=task)
    # Test the gold query
    with open('example_task_1_gold_query.sql', 'r') as f:
        gold_query = f.read()
    cursor = agent.conn.cursor()
    cursor.execute(gold_query)

    # Fetch and display results
    results = cursor.fetchall()
    print(f"\nQuery returned {len(results)} results:\n")

    # Print header
    print(f"{'Employer':<40} {'Attorney Email':<35} {'Cases':<8} {'Certified':<10} {'Success %':<10}")
    print("-" * 110)

    # Print first 10 results
    for row in results[:10]:
        employer, email, case_load, certified, success_rate = row
        employer_short = employer[:38] if len(employer) > 38 else employer
        email_short = email[:33] if len(email) > 33 else email
        print(f"{employer_short:<40} {email_short:<35} {case_load:<8} {certified:<10} {success_rate:<10}")

    if len(results) > 10:
        print(f"\n... and {len(results) - 10} more results")

    cursor.close()
    agent.conn.close()
    print("\n" + "="*80)


if __name__ == "__main__":
    main()