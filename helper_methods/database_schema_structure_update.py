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

run_scenarios = [10]

# The CNP of the user you want to delete
cnp = "0012"


class ScenarioRunner:
    def __init__(self, cnp=None):
        self.cnp = cnp

    def run_scenario(self, scenario):
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
        else:
            raise ValueError(f"Invalid value for scenario: {scenario}, look at the valid options above.")


if __name__ == "__main__":
    scenario_runner = ScenarioRunner(cnp)

    for run_scenario in run_scenarios:
        try:
            scenario_runner.run_scenario(run_scenario)
            print(f"Scenario {run_scenario} has been executed.")
        except ValueError as ve:
            print(f"An error occurred: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred while executing scenario {run_scenario}: {e}")

    print("All scenarios have been executed.")
