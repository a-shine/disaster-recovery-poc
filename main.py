import matching_mechanism

if __name__ == "__main__":
    matching_mechanism.region_to_many_recovery("europe-west3")


# The high-level drp plan is synchronouse:
# 1. detect a disaster -> declare DR status (prevent VM creation other than by the DR plan)
# 2. identify workload pairs to swicth
# 3. switch workload pairs
