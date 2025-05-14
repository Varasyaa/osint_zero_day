# Fetch past scans
recent = collection.find().sort("_id", -1).limit(5)
for entry in recent:
    print(entry)
