from pocketbase import PocketBase  # Client also works the same
from pocketbase.client import FileUpload

client = PocketBase('http://127.0.0.1:8090')

admin_data = client.admins.auth_with_password("jemcarlo46@gmail.com", "password123")
print(admin_data.is_valid)


# result = client.collection("example").get_list(1, 50,
#  {"filter": 'status = true'} )getFullList
result = client.collection("example").get_full_list(
    query_params={"filter": "status = true"}
)
for record in result:
    print(f"ID: {record.id}")
    print(f"Status: {record.status}")
    print(f"Created: {record.created}")
    print(f"Updated: {record.updated}")
    print("-" * 20)



