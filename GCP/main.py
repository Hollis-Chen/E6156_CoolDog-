from fastapi import FastAPI, HTTPException, Path
from google.cloud import firestore

app = FastAPI()

# Initialize Firestore client
db = firestore.Client()


@app.get("/")
async def read_root():
    return {"message": "Hello from groups"}


@app.get("/groups/{group_id}")
async def read_group(group_id: int = Path(..., title="The ID of the group", ge=1, le=1000)):
    group_ref = db.collection('groups').document(str(group_id))
    group = group_ref.get()
    if group.exists:
        return group.to_dict()
    raise HTTPException(status_code=404, detail="Group not found")


@app.post("/groups/")
async def create_group(group: dict):
    # Check if the 'id' field is present in the input data
    if 'id' not in group:
        raise HTTPException(status_code=400, detail="ID is required for creating a group")

    # Assuming you have an "id" field in your input data
    group_id = group['id']

    # Convert the integer ID to a string
    group_id_str = str(group_id)

    # Check if the group_id already exists
    existing_group = db.collection('groups').document(group_id_str).get()
    if existing_group.exists:
        raise HTTPException(status_code=400, detail=f"Group with ID {group_id} already exists")

    # If the group_id is not provided, Firestore will generate a random one
    new_group_ref = db.collection('groups').document(group_id_str).set(group)

    # If the group_id is not provided, use the generated ID from Firestore
    if not group_id:
        group_id = new_group_ref.id

    new_group_data = group.copy()
    new_group_data["id"] = group_id
    return new_group_data


@app.put("/groups/{group_id}")
async def update_group(group_id: int, updated_group: dict):
    group_ref = db.collection('groups').document(str(group_id))
    group = group_ref.get()
    if group.exists:
        # Exclude the 'id' field from the updated_group dictionary
        updated_group.pop("id", None)

        # Update the document in Firestore
        group_ref.update(updated_group)

        # Return the updated group including the ID
        return {"id": group_id, **updated_group}

    raise HTTPException(status_code=404, detail="Group not found")


@app.delete("/groups/{group_id}")
async def delete_group(group_id: int):
    group_ref = db.collection('groups').document(str(group_id))
    group = group_ref.get()
    if group.exists:
        deleted_group = {"id": group_id, **group.to_dict()}
        group_ref.delete()
        return deleted_group
    raise HTTPException(status_code=404, detail="Group not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8012)
