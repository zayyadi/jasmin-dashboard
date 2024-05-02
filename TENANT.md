# HOW TO SETUP PUBLIC AND TENANTS

## ACTIVATE VIRTUAL ENVIRONMENT


- Firstly you migrate the tenants models to the db `python manage migrate --shared` after which the model has been migrated, you will create a public schema by using django shell:

`python manage.py shell` after then import **Client** and **Domain** models `from main.tenants.models import Client, Domain`

`tenant = Client(schema_name="public",name="public", jasmin_host="localhost", jasmin_port=8990, jasmin_username="admin", jasmin_password="admin",description="public")`
`tenant.save`
`domain = Domain(domain="localhost", tenant=tenant, is_primary=True)`
it will create a public schema, now start your 