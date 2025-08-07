from project import create_app, db
from project.models.models import Category, SubCategory, Product, ProductAttribute, PriceHistory, AggregatedReview
import click

app = create_app()

@app.cli.command('init-db')
def init_db():
    """Initialize the database with tables."""
    with app.app_context():
        db.create_all()
        click.echo('Database initialized! Use init_db.py script to populate with sample data.')

if __name__ == '__main__':
    # Run with simpler settings to avoid hanging
    app.run(debug=False, host='127.0.0.1', port=5001, threaded=True) 