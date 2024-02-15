
from specklepy.api.wrapper import StreamWrapper
from specklepy.api import operations
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Speckle Stream URL
stream_url = "https://macad.speckle.xyz/streams/4036f9f8de"

# Set up the wrapper, client and transport
wrapper = StreamWrapper(stream_url)
client = wrapper.get_client()
transport = wrapper.get_transport()

# Find the Branch
branch = client.branch.get(wrapper.stream_id, name="my_building")
print("The branch is: " + str(branch))

# Get the ID of the Referenced Object in the lastest commit of the Branch
objID = branch.commits.items[0].referencedObject
print("The objID is: " + str(objID))

# Get the data that is nested inside
nested_object_id = "3ac0c828ff911d3e55f2e674f2654c71"
objData = operations.receive( nested_object_id, transport)
print("The objData is: " + str(objData))

# View all the categories available
objData_names = objData.get_dynamic_member_names()
print("The Speckle Objects inside are called: "+ str(objData_names))

# Store the elements from those categories
slabs = objData["Slabs"]
columns = objData["Columns"]
walls = objData["Walls"]

# See the parameters of those categories
slab_parameters = slabs[0].get_member_names()
print(slab_parameters)

# Extract the parameter values into lists
costs, volumes, materials = [], [], []
for component in [slabs, walls, columns]:
    for s in component:
        costs.append(s['Cost'])
        volumes.append(s['Volume'])
        materials.append(s['Material'])

# Add up the volumes of each material type
material_volumes = {}
for material, volume in zip(materials, volumes):
    if material in material_volumes:
        material_volumes[material] += volume
    else:
        material_volumes[material] = volume

# Transform that into a table and create a Pie Chart
material_volumes = pd.Series(material_volumes)
#print(material_volumes)

sns.set_style("whitegrid")
plt.figure(figsize=(8,8))
plt.pie(material_volumes, labels=material_volumes.index, autopct='%1.1f%%')
plt.title("Material Distribution by Volume")
plt.show()