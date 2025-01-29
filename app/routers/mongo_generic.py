from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.dependencies.mongodb import get_mongo_client, MONGO_DB

router = APIRouter(
    prefix="/mongo",
    tags=["MongoDB Generic CRUD"]
)


@router.get("/{collection_name}")
def read_all_documents(collection_name: str, mongo_client=Depends(get_mongo_client)):
    collection = mongo_client[MONGO_DB][collection_name]
    documents = list(collection.find({}))
    # Convert ObjectId to string for JSON serialization
    for doc in documents:
        doc["_id"] = str(doc["_id"])
    return documents


@router.post("/{collection_name}")
def create_document(collection_name: str, data: dict, mongo_client=Depends(get_mongo_client)):
    collection = mongo_client[MONGO_DB][collection_name]
    result = collection.insert_one(data)
    return {"inserted_id": str(result.inserted_id), "data": data}


@router.put("/{collection_name}/{doc_id}")
def update_document(collection_name: str, doc_id: str, data: dict, mongo_client=Depends(get_mongo_client)):
    collection = mongo_client[MONGO_DB][collection_name]

    if not ObjectId.is_valid(doc_id):
        raise HTTPException(status_code=400, detail="Invalid document ID")

    result = collection.update_one({"_id": ObjectId(doc_id)}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"updated_id": doc_id, "new_data": data}


@router.delete("/{collection_name}/{doc_id}")
def delete_document(collection_name: str, doc_id: str, mongo_client=Depends(get_mongo_client)):
    collection = mongo_client[MONGO_DB][collection_name]

    if not ObjectId.is_valid(doc_id):
        raise HTTPException(status_code=400, detail="Invalid document ID")

    result = collection.delete_one({"_id": ObjectId(doc_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"deleted_id": doc_id}
