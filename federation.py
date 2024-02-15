
from specklepy.api.client import SpeckleClient
from specklepy.api import operations
from specklepy.api.wrapper import StreamWrapper
from specklepy.objects import Base

# This script will combine the latest commit of each branch 
# and push it into a new branch of your choice.
# Dont forget to change your token and stream_url before running! :)

# Our MaCAD server!
server_url = "YOUR SERVER URL"
# The token for your account. Get it from the Speckle Dashboard > Profile > Acess Tokens
token = "YOUR TOKEN HERE"
# This is the stream you want to federate the branches of. Change it to your studio stream! 
stream_url = "YOUR STREAM URL"
# The name of the branch you want to push to. The data inside it will be ignored on further pushes.
federated_branch = "federated_commits"
# A list containing branch names that you dont want federated. Change this according to your stream.
filter_branches = [ "site/00-federated-model", "students/g01-site_locations", "students/g12-geometry", "students/combined-site-locations", "federated", "federated", "students/site_test"]

# Authenticate the account with the token (for servers or remote scripts that don´t have access to your local speckle account)
client = SpeckleClient(host=server_url)
client.authenticate_with_token(token)

# Get the stream object and a transport object
wrapper = StreamWrapper(stream_url)
stream_id = wrapper.stream_id
transport = wrapper.get_transport()

# Get the branch objects, their names and their IDs
branches = client.branch.list(stream_id, 50)
branches_ids = [branch.id for branch in branches]
branches_names = [branch.name for branch in branches]

# Lets beggin with an empty list to store the commit IDs
referenced_objects_ids = []
# Now we loop through each branch, get the latest commit (obj_id) 
# and extract their referenced_object (the geometry data itself!)
for branch in branches:
    # Match branch.name to the names of the branches you dont want to federate
    if branch.name in filter_branches:
        continue
    # If the branch is not empty, get the referenced object ID of the latest commit
    if len(branch.commits.items) > 0:
        print(f"federating branch named {branch.name}")
        obj_id = branch.commits.items[0].referencedObject
        referenced_objects_ids.append(obj_id)
    # If the branch is empty, ignore it
    else:
        print(f"{branch.name} was empty, ignoring")
        continue

print(f"Got data from {len(referenced_objects_ids)} branches")

# Now that we have the referenced_objects IDs, we can pass it to the operations.receive method to get the actual data
commit_data = [operations.receive(obj_id=ref_obj, remote_transport=transport) for ref_obj in referenced_objects_ids]
#commit_data = operations.receive(obj_id=referenced_objects_ids[0])
print("Received all data")

# Now we create a Speckle Object (its called Base in speckle lingo)
federated_commit_object = Base(speckle_type="Federation.Granular")

# We put the commit_data inside of it
federated_commit_object["@Components"] = commit_data

# We send it to the Speckle Server DB to get a unique identifier for this speckle object
# Remember...commits dont hold data in themselves...They point to objects in the database!
hash3 = operations.send(base=federated_commit_object , transports=[transport])

# We create a function just to handle the two type of situations:
# If the federated branch already exists, we push into it
# If it doesnt exist yet (first time you run this), we create it
def try_get_branch_or_create(client, stream_id, branch_name):
    branch = client.branch.get(stream_id=stream_id, name=branch_name)
    if not branch:
        branch = client.branch.create(stream_id=stream_id, name=branch_name)
    return branch

# We use that function to get the branch
branch = try_get_branch_or_create(client, stream_id, federated_branch)

# And finally we are ready to create our commit!
commit_id3 = client.commit.create(
    branch_name=branch,
    stream_id=stream_id,
    object_id=hash3,
    message="Automated federated commit",
)

print("Made a new commit")