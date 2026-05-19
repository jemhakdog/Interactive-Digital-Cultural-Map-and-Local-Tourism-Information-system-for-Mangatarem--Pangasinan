import os
import sys

# Ensure project root is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from modules.attractions.models import AttractionReview
from modules.business.models import Establishment, EstablishmentReview

app = create_app()

with app.app_context():
    print("Connecting to the database and starting review migration...")
    
    # 1. Update Attraction Reviews
    pending_attraction_reviews = AttractionReview.query.filter_by(status="pending").all()
    attraction_count = len(pending_attraction_reviews)
    for review in pending_attraction_reviews:
        review.status = "approved"
    
    # 2. Update Establishment Reviews
    pending_establishment_reviews = EstablishmentReview.query.filter_by(status="pending").all()
    establishment_count = len(pending_establishment_reviews)
    for review in pending_establishment_reviews:
        review.status = "approved"
        
    db.session.commit()
    print(f"Successfully migrated {attraction_count} attraction reviews to 'approved'.")
    print(f"Successfully migrated {establishment_count} establishment reviews to 'approved'.")
    
    # 3. Recalculate Establishment Ratings
    print("Recalculating establishment rating averages...")
    all_establishments = Establishment.query.all()
    for est in all_establishments:
        approved_reviews = EstablishmentReview.query.filter_by(
            establishment_id=est.id, status="approved"
        ).all()
        if approved_reviews:
            est.rating_avg = sum(r.rating for r in approved_reviews) / len(approved_reviews)
            est.review_count = len(approved_reviews)
        else:
            est.rating_avg = 0
            est.review_count = 0
            
    db.session.commit()
    print("Recalculation complete. Ratings successfully refreshed in database.")
