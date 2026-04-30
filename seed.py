"""
Initialize the database schema and load data from data/ CSVs.
Usage: python seed.py
"""
from app import create_app, db


def init_db():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        print('✓ Database schema initialized.')

    import extract_project_costs
    print('Extracting project CAPEX/OPEX data to CSV...')
    extract_project_costs.main()

    from load_data import load_all
    load_all()


if __name__ == '__main__':
    init_db()
