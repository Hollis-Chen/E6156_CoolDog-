from fastapi import FastAPI, HTTPException, Path
import json
import os

app = FastAPI()

# Read data from the JSON file
data_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "", "groups.json")

with open(data_file, "r") as file:
    groups = json.load(file)

@app.on_event("shutdown")
def save_data_on_shutdown():
    # Save the data back to the JSON file when the application shuts down
    with open(data_file, "w") as file:
        json.dump(groups, file, indent=2)

@app.get("/")
async def read_root():
    return {"message": "Hello from groups"}

@app.get("/groups/{group_id}")
async def read_group(group_id: int = Path(..., title="The ID of the group", ge=1, le=1000)):
    group = next((item for item in groups if item["id"] == group_id), None)
    if group:
        return group
    raise HTTPException(status_code=404, detail="Group not found")

@app.post("/groups/")
async def create_group(group: dict):
    new_id = max(item["id"] for item in groups) + 1
    group["id"] = new_id
    groups.append(group)
    return group

@app.put("/groups/{group_id}")
async def update_group(group_id: int, updated_group: dict):
    group_index = next((index for index, item in enumerate(groups) if item["id"] == group_id), None)
    if group_index is not None:
        groups[group_index] = updated_group
        return updated_group
    raise HTTPException(status_code=404, detail="Group not found")

@app.delete("/groups/{group_id}")
async def delete_group(group_id: int):
    group_index = next((index for index, item in enumerate(groups) if item["id"] == group_id), None)
    if group_index is not None:
        deleted_group = groups.pop(group_index)
        return deleted_group
    raise HTTPException(status_code=404, detail="Group not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
