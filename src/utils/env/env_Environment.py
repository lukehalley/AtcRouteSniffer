import os

# Get the max task we can run at a time which we set
def getBlockRange():
    return int(os.getenv('BLOCK_RANGE'))