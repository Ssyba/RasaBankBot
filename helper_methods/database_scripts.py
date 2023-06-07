import queries_location

# Change the value of run_scenario depending on the query you want to run
# Users table #
# 1 - create the users table
# 2 - delete the users table
# 3 - clear data from users table
# 4 - delete a user by CNP
# 5 - add random users to the user table by cnp
# Bills table #
# 6 - create bills table
# 7 - delete bills table
# 8 - clear data from bills table
# 9 - populate the bills table with mock data for each user in the users table
# 10 - add random taxes to each field in the bills table

RUN_SCENARIOS = [5]

# The CNP of the user you want to delete
CNP = "0001"
NUMBER_OF_USERS = 100


class ScenarioRunner:
    def __init__(self, cnp=None, number_of_users=0):
        self.cnp = cnp
        self.number_of_users = number_of_users

    def run_scenario(self, scenario):
        # Users table
        if scenario == 1:
            queries_location.create_users_table_query()
        elif scenario == 2:
            queries_location.delete_users_table_query()
        elif scenario == 3:
            queries_location.clear_data_users_table_query()
        elif scenario == 4:
            queries_location.delete_user_by_cnp_query(self.cnp)
        elif scenario == 5:
            queries_location.insert_random_user_query(self.cnp)

        # Bills table
        elif scenario == 6:
            queries_location.create_bills_table_query()
        elif scenario == 7:
            queries_location.delete_bills_table_query()
        elif scenario == 8:
            queries_location.clear_data_bills_table_query()
        elif scenario == 9:
            queries_location.fill_bills_table_query()
        elif scenario == 10:
            queries_location.update_bills_table_with_random_taxes_query()

        # Transactions table
        elif scenario == 11:
            queries_location.create_transactions_table_query()
        elif scenario == 12:
            queries_location.delete_transactions_table_query()
        elif scenario == 13:
            queries_location.clear_data_transactions_table_query()

        # Credit cards table
        elif scenario == 14:
            queries_location.create_credit_cards_table_query()
        elif scenario == 15:
            queries_location.delete_credit_cards_table_query()
        elif scenario == 16:
            queries_location.clear_credit_cards_table_query()
        elif scenario == 17:
            queries_location.generate_random_credit_cards_for_users()

        # Feedback table
        elif scenario == 18:
            queries_location.create_feedback_table_query()
        elif scenario == 19:
            queries_location.delete_feedback_table_query()
        elif scenario == 20:
            queries_location.clear_feedback_table_query()

        # Populate tables
        elif scenario == 21:
            queries_location.populate_users_table(self.number_of_users)
        else:
            raise ValueError(f"Invalid value for scenario: {scenario}, look at the valid options above.")


if __name__ == "__main__":
    scenario_runner = ScenarioRunner(CNP)

    for run_scenario in RUN_SCENARIOS:
        try:
            scenario_runner.run_scenario(run_scenario)
            print(f"Scenario {run_scenario} has been executed.")
        except ValueError as ve:
            print(f"An error occurred: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred while executing scenario {run_scenario}: {e}")

    print("Script has finished.")
