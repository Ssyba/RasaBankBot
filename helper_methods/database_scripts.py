import queries_location

# Change the value of run_scenario depending on the query you want to run
# Users table #
# 1 - create the users table
# 2 - delete the users table
# 3 - clear data from users table
# 4 - add random users to the user table by cnp (uses the CNP global variable)
# 5 - delete a user by cnp (uses the CNP global variable)

# Bills table #
# 6 - create bills table
# 7 - delete bills table
# 8 - clear data from bills table
# 9 - add random taxes for user by cnp (uses the CNP global variable)

# Transactions table
# 10 - create transactions table
# 11 - delete transactions table
# 12 - clear data from the transactions table

# Credit cards table
# 13 - create credit cards table
# 14 - delete credit cards table
# 15 - clear credit cards table
# 16 - add random credit card by user cnp (uses the CNP global variable)

# Feedback table
# 17 - create feedback table
# 18 - delete feedback table
# 19 - clear feedback table

# Populate tables
# 20 - populate users table (uses the NUMBER_OF_USERS global variable)
# 21 - populate bills table
# 22 - populate transactions table
# 23 - populate credit cards table
# 24 - populate feedback table


# Global variables
CNP = "0001"
NUMBER_OF_USERS = 10

# Scenarios that you wish to run
RUN_SCENARIOS = [24]


class ScenarioRunner:
    def __init__(self, cnp=None, number_of_users=0):
        self.cnp = CNP
        self.number_of_users = NUMBER_OF_USERS

    def run_scenario(self, scenario):
        # Users table
        if scenario == 1:
            queries_location.create_users_table_query()
        elif scenario == 2:
            queries_location.delete_users_table_query()
        elif scenario == 3:
            queries_location.clear_data_users_table_query()
        elif scenario == 4:
            queries_location.insert_user_by_cnp_query(self.cnp)
        elif scenario == 5:
            queries_location.delete_user_by_cnp_query(self.cnp)

        # Bills table
        elif scenario == 6:
            queries_location.create_bills_table_query()
        elif scenario == 7:
            queries_location.delete_bills_table_query()
        elif scenario == 8:
            queries_location.clear_data_bills_table_query()
        elif scenario == 9:
            queries_location.insert_bills_by_cnp_query(self.cnp)

        # Transactions table
        elif scenario == 10:
            queries_location.create_transactions_table_query()
        elif scenario == 11:
            queries_location.delete_transactions_table_query()
        elif scenario == 12:
            queries_location.clear_data_transactions_table_query()

        # Credit cards table
        elif scenario == 13:
            queries_location.create_credit_cards_table_query()
        elif scenario == 14:
            queries_location.delete_credit_cards_table_query()
        elif scenario == 15:
            queries_location.clear_credit_cards_table_query()
        elif scenario == 16:
            queries_location.insert_credit_card_by_cnp_query(self.cnp)

        # Feedback table
        elif scenario == 17:
            queries_location.create_feedback_table_query()
        elif scenario == 18:
            queries_location.delete_feedback_table_query()
        elif scenario == 19:
            queries_location.clear_feedback_table_query()

        # Populate tables
        elif scenario == 20:
            queries_location.populate_users_table_query(self.number_of_users)
        elif scenario == 21:
            queries_location.populate_bills_table_query()
        elif scenario == 22:
            queries_location.populate_transactions_table_query()
        elif scenario == 23:
            queries_location.populate_credit_cards_table_query()
        elif scenario == 24:
            queries_location.populate_feedback_table_query()

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
