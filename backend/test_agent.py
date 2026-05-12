from agent import handle_query

query = input("Ask something: ")

response = handle_query(query)

print("\n")
print(response)