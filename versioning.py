from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.api.wrapper import StreamWrapper
import pandas as pd

# This script works with conjunction with plot_versioning.py
# This one will get the commit history in a stream and create a csv file to store it
# plot_versioning.py will turn that csv into a nice plot of commit history!

# Our MaCAD server!
server_url = "YOUR SERVER URL"

#This is the stream you want to plot the history of. 
# Try changing it to your studio stream! 
stream_url = "YOUR STREAM URL"

# Authenticate with the default account on your computer
# (Just an alternative method to authenticate to the one in federation.py)
# It will use your computer speckle account
client = SpeckleClient(host = server_url)
account = get_default_account()
client.authenticate_with_account(account)

# Get the stream ID so you can fetch the stream object itself
wrapper = StreamWrapper (stream_url)
stream_id = wrapper.stream_id 
stream = client.stream.get(id=stream_id)

# Now we are ready to begging extracting the data we will want to plot
streamName = stream.name
collaborators = stream.collaborators
collaborators_names = [col.name for col in collaborators]
branches = client.branch.list(stream_id, 100)
branchesNames =  [branch.name for branch in branches]
branch_index = {branch.name: i for i, branch in enumerate(branches)}

# Get all the commits in the stream
commits = client.commit.list(stream_id, 100)
# Create an empty list to store the information we are about to extract
commit_data = []
# For each commit, we create a dictionary (commit_info) that will become a row in our CSV.
# I also do some fancy things to the date format! Dont worry too much about that :)
for commit in commits:
    commit_date = commit.createdAt
    formatted_date = commit_date.strftime("%d-%m-%Y")
    branch_name = commit.branchName
    author = commit.authorName
    message = commit.message
    software = commit.sourceApplication

    # Store it in the dictionary
    commit_info = {"commit_id": commit.id, 
                    "author": author,
                    "software": software,
                    "date": formatted_date, 
                    "message": message,
                    "branch": branch_name}
    # Save it to the commit_data list
    commit_data.append(commit_info)

# We have everything on our side now!
# All we have to do is transform it into a dataframe and save it to a CSV
commit_df = pd.DataFrame(commit_data)
commit_df['date'] = pd.to_datetime(commit_df['date'], format="%d-%m-%Y")

# Sort the DataFrame by branch and date: because the last step is never the last step! :)
# To make it tidy, we organize out data by branch and date
commit_df = commit_df.sort_values(by=['branch', 'date'])

# Export!
commit_df.to_csv("commit_data.csv", index=False)

print("Finished")