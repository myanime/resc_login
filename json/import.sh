mongo <<'EOF'
use database
db.sites.drop()
EOF
mongoimport -d database -c sites dreammarket_document.json
mongoimport -d database -c sites rescator_document.json
mongoimport -d database -c sites hansa_document.json