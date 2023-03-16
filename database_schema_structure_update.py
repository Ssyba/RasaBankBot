import queries_location

# This is done so that I can run each query from pycharm with a click of a button

# Change the value of run_scenario depending on the query you want to run
# 1 - create the users table
# 2 - delete the users table
# 3 - delete a user by CNP
run_scenarios = [3]

# The CNP of the user you want to delete
cnp = "0002"

if __name__ == "__main__":
    try:
        for run_scenario in run_scenarios:
            if run_scenario == 1:
                # Create the users table
                queries_location.create_users_table_query()
            elif run_scenario == 2:
                # Delete the users table
                queries_location.delete_users_table_query()
            elif run_scenario == 3:
                # Delete a user by CNP
                queries_location.delete_user_by_cnp(cnp)
            else:
                print(f"Invalid value for run_scenario: {run_scenario}, look at the valid options above.")
        print("All scenarios have been executed.")
    except Exception as e:
        print(f"An error occurred while executing the scenarios: {run_scenario}")
        print("All other scenarios have been executed.")
