from app import create_app

app = create_app()

print("Registered routes:")
for rule in app.url_map.iter_rules():
    print(f"  {rule.rule} -> {rule.endpoint}")

print(f"\nTotal routes: {len(list(app.url_map.iter_rules()))}") 