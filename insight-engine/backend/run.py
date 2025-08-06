from project import create_app, db
from project.models import AITool, LuxuryAppliance, AggregatedReview
import click

app = create_app()

@app.cli.command('init-db')
def init_db():
    """Initialize the database with tables."""
    with app.app_context():
        db.create_all()
        click.echo('Database initialized!')

@app.cli.command('seed-ai-tools')
def seed_ai_tools():
    """Seed the database with sample AI tools with insights."""
    with app.app_context():
        # Clear existing data
        AggregatedReview.query.delete()
        AITool.query.delete()
        
        # Sample AI tools with insights
        tools = [
            AITool(
                name='ChatGPT',
                website='https://chat.openai.com',
                short_description='Advanced language model for conversation and text generation',
                pricing_model='Freemium',
                primary_use_case='Content Creation',
                insight_snippet='Revolutionary AI that excels at creative writing and brainstorming, but users note occasional factual inaccuracies.',
                ideal_for_tags='Content Creators, Students, Researchers, Business Professionals'
            ),
            AITool(
                name='Midjourney',
                website='https://midjourney.com',
                short_description='AI-powered image generation from text descriptions',
                pricing_model='Subscription',
                primary_use_case='Image Generation',
                insight_snippet='Produces stunning artistic images with incredible detail, though the learning curve for prompts can be steep.',
                ideal_for_tags='Artists, Designers, Marketers, Creative Professionals'
            ),
            AITool(
                name='GitHub Copilot',
                website='https://github.com/features/copilot',
                short_description='AI-powered code completion and generation',
                pricing_model='Subscription',
                primary_use_case='Development',
                insight_snippet='Dramatically speeds up coding workflow, but some developers worry about over-reliance and code quality.',
                ideal_for_tags='Developers, Software Engineers, Programming Students'
            ),
            AITool(
                name='Notion AI',
                website='https://notion.so',
                short_description='AI-powered writing and content creation within Notion',
                pricing_model='Subscription',
                primary_use_case='Content Creation',
                insight_snippet='Seamlessly integrates AI writing into existing workflows, though the output sometimes needs human refinement.',
                ideal_for_tags='Productivity Enthusiasts, Teams, Project Managers'
            ),
            AITool(
                name='Jasper',
                website='https://jasper.ai',
                short_description='AI content creation platform for marketing and business',
                pricing_model='Subscription',
                primary_use_case='Content Creation',
                insight_snippet='Excellent for marketing copy and business content, with strong templates but can be expensive for small teams.',
                ideal_for_tags='Marketers, Business Owners, Content Teams, Agencies'
            )
        ]
        
        for tool in tools:
            db.session.add(tool)
        
        db.session.commit()
        click.echo('AI tools seeded with insights!')

@app.cli.command('seed-luxury-appliances')
def seed_luxury_appliances():
    """Seed the database with luxury appliance brands and models with insights."""
    with app.app_context():
        # Clear existing data
        AggregatedReview.query.delete()
        LuxuryAppliance.query.delete()
        
        # Sample luxury appliances with insights
        appliances = [
            LuxuryAppliance(
                name='Dacor 48" Professional Range',
                brand='Dacor',
                category='Ranges',
                model_number='DR48P',
                msrp=10000,
                price_range='$8,000 - $12,000',
                website='https://www.dacor.com/ranges/professional-ranges',
                description='Professional-grade range with dual fuel capabilities and precision cooking',
                features='Dual fuel; Convection oven; 6 burners; Precision temperature control',
                design_style='Professional',
                finish_options='Stainless Steel; Black Stainless',
                dimensions='48" W x 27" D x 36" H',
                energy_rating='Energy Star certified',
                warranty='Limited 2-year warranty',
                insight_snippet='Praised for its precise temperature control and professional-grade performance, but some owners note the high price point.',
                style_tags='Professional, Modern, High-End'
            ),
            LuxuryAppliance(
                name='Sub-Zero 48" Built-In Refrigerator',
                brand='Sub-Zero',
                category='Refrigerators',
                model_number='BI-48S',
                msrp=15000,
                price_range='$12,000 - $18,000',
                website='https://www.subzero-wolf.com/refrigerators',
                description='Professional built-in refrigerator with dual cooling systems',
                features='Dual cooling; Air purification; Built-in design; Panel ready',
                design_style='Luxury',
                finish_options='Stainless Steel; Panel Ready; Custom finishes',
                dimensions='48" W x 24" D x 84" H',
                energy_rating='Energy Star certified',
                warranty='Limited 5-year warranty',
                insight_snippet='Whisper-quiet operation and excellent food preservation, but the ice maker can be slow and maintenance is expensive.',
                style_tags='Luxury, Built-In, Professional'
            ),
            LuxuryAppliance(
                name='Wolf 48" Dual Fuel Range',
                brand='Wolf',
                category='Ranges',
                model_number='DF486',
                msrp=12500,
                price_range='$10,000 - $15,000',
                website='https://www.subzero-wolf.com/ranges',
                description='Professional dual fuel range with gas burners and electric oven',
                features='Dual fuel; 6 burners; Convection oven; Infrared broiler',
                design_style='Professional',
                finish_options='Stainless Steel; Black Stainless',
                dimensions='48" W x 27" D x 36" H',
                energy_rating='Professional grade',
                warranty='Limited 2-year warranty',
                insight_snippet='Exceptional cooking performance with precise control, though the learning curve for the dual fuel system can be challenging.',
                style_tags='Professional, Dual Fuel, High-Performance'
            ),
            LuxuryAppliance(
                name='Thermador 36" Freedom Refrigerator',
                brand='Thermador',
                category='Refrigerators',
                model_number='T36IR800SP',
                msrp=10000,
                price_range='$8,000 - $12,000',
                website='https://www.thermador.com/refrigerators',
                description='Freedom refrigerator with column design and advanced features',
                features='Column design; Freedom system; LED lighting; Advanced cooling',
                design_style='Modern',
                finish_options='Stainless Steel; Panel Ready; Black Stainless',
                dimensions='36" W x 30" D x 70" H',
                energy_rating='Energy Star certified',
                warranty='Limited 2-year warranty',
                insight_snippet='Innovative column design offers great flexibility, but the Freedom system can be complex to configure initially.',
                style_tags='Modern, Flexible, Innovative'
            ),
            LuxuryAppliance(
                name='Viking 48" Professional Range',
                brand='Viking',
                category='Ranges',
                model_number='VGR548',
                msrp=11500,
                price_range='$9,000 - $14,000',
                website='https://www.vikingrange.com/ranges',
                description='Professional range designed for serious cooking enthusiasts',
                features='6 burners; Convection oven; Infrared broiler; Heavy-duty construction',
                design_style='Professional',
                finish_options='Stainless Steel; Black',
                dimensions='48" W x 27" D x 36" H',
                energy_rating='Professional grade',
                warranty='Limited 2-year warranty',
                insight_snippet='Built like a tank with commercial-grade performance, though some find the controls less intuitive than competitors.',
                style_tags='Professional, Commercial-Grade, Durable'
            ),
            LuxuryAppliance(
                name='Fisher & Paykel 36" DishDrawer',
                brand='Fisher & Paykel',
                category='Dishwashers',
                model_number='DD60DAX9N',
                msrp=2000,
                price_range='$1,500 - $2,500',
                website='https://www.fisherpaykel.com/dishwashers',
                description='Innovative drawer-style dishwasher with flexible loading',
                features='Drawer design; Flexible loading; Quiet operation; Energy efficient',
                design_style='Modern',
                finish_options='Stainless Steel; Panel Ready',
                dimensions='36" W x 24" D x 34" H',
                energy_rating='Energy Star certified',
                warranty='Limited 2-year warranty',
                insight_snippet='Revolutionary drawer design is incredibly convenient, but the smaller capacity means more frequent loading.',
                style_tags='Modern, Innovative, Convenient'
            ),
            LuxuryAppliance(
                name='Monogram 30" Built-In Refrigerator',
                brand='Monogram',
                category='Refrigerators',
                model_number='ZISB30DRSS',
                msrp=7500,
                price_range='$6,000 - $9,000',
                website='https://www.monogram.com/refrigerators',
                description='Built-in refrigerator with advanced cooling and storage',
                features='Built-in design; Advanced cooling; LED lighting; Flexible storage',
                design_style='Contemporary',
                finish_options='Stainless Steel; Panel Ready',
                dimensions='30" W x 24" D x 84" H',
                energy_rating='Energy Star certified',
                warranty='Limited 2-year warranty',
                insight_snippet='Excellent integration with custom cabinetry, though the premium price may not justify the features for some buyers.',
                style_tags='Contemporary, Built-In, Custom'
            ),
            LuxuryAppliance(
                name='SKS 48" Professional Range',
                brand='SKS',
                category='Ranges',
                model_number='SKS48P',
                msrp=9000,
                price_range='$7,000 - $11,000',
                website='https://www.sks.com/ranges',
                description='Professional range with commercial-grade features',
                features='Commercial-grade burners; Convection oven; Heavy-duty construction',
                design_style='Professional',
                finish_options='Stainless Steel; Black',
                dimensions='48" W x 27" D x 36" H',
                energy_rating='Professional grade',
                warranty='Limited 2-year warranty',
                insight_snippet='Great value for professional features, though the brand recognition is lower than some competitors.',
                style_tags='Professional, Value, Commercial-Grade'
            ),
            LuxuryAppliance(
                name='JennAir 36" French Door Refrigerator',
                brand='JennAir',
                category='Refrigerators',
                model_number='JFC2290REP',
                msrp=5500,
                price_range='$4,000 - $7,000',
                website='https://www.jennair.com/refrigerators',
                description='Premium French door refrigerator with advanced features',
                features='French doors; Bottom freezer; LED lighting; Advanced cooling',
                design_style='Modern',
                finish_options='Stainless Steel; Panel Ready; Black Stainless',
                dimensions='36" W x 30" D x 70" H',
                energy_rating='Energy Star certified',
                warranty='Limited 1-year warranty',
                insight_snippet='Good balance of features and price, though the warranty is shorter than premium competitors.',
                style_tags='Modern, Balanced, Accessible'
            ),
            LuxuryAppliance(
                name='Gaggenau 30" Built-In Oven',
                brand='Gaggenau',
                category='Ovens',
                model_number='BS491',
                msrp=10000,
                price_range='$8,000 - $12,000',
                website='https://www.gaggenau.com/ovens',
                description='Premium built-in oven with advanced cooking technology',
                features='Built-in design; Advanced cooking modes; Precise temperature control',
                design_style='Luxury',
                finish_options='Stainless Steel; Panel Ready; Custom finishes',
                dimensions='30" W x 24" D x 24" H',
                energy_rating='Energy Star certified',
                warranty='Limited 2-year warranty',
                insight_snippet='Ultra-premium quality with exceptional precision, but the high price and complex controls may intimidate casual cooks.',
                style_tags='Luxury, Ultra-Premium, Precision'
            )
        ]
        
        for appliance in appliances:
            db.session.add(appliance)
        
        db.session.commit()
        click.echo('Luxury appliances seeded with insights!')

@app.cli.command('seed-reviews')
def seed_reviews():
    """Seed the database with sample aggregated reviews."""
    with app.app_context():
        # Clear existing reviews
        AggregatedReview.query.delete()
        
        # Sample reviews for AI tools
        ai_tool_reviews = [
            AggregatedReview(
                ai_tool_id=1,  # ChatGPT
                overall_rating=4.5,
                ease_of_use_score=4.8,
                feature_score=4.6,
                value_for_money_score=4.2,
                positive_sentiment_summary='Users love the conversational interface and creative capabilities',
                negative_sentiment_summary='Concerns about factual accuracy and subscription costs',
                key_insights='Revolutionary conversational AI that excels at creative tasks',
                common_complaints='Factual inaccuracies, expensive subscription',
                standout_features='Natural conversation, creative writing, code assistance',
                total_reviews_analyzed=150
            ),
            AggregatedReview(
                ai_tool_id=2,  # Midjourney
                overall_rating=4.7,
                ease_of_use_score=3.9,
                feature_score=4.9,
                value_for_money_score=4.1,
                positive_sentiment_summary='Stunning image quality and artistic capabilities',
                negative_sentiment_summary='Steep learning curve for prompts',
                key_insights='Produces incredible artistic images but requires prompt expertise',
                common_complaints='Complex prompt system, Discord-only interface',
                standout_features='Artistic quality, detailed images, creative control',
                total_reviews_analyzed=120
            )
        ]
        
        # Sample reviews for luxury appliances
        appliance_reviews = [
            AggregatedReview(
                luxury_appliance_id=1,  # Dacor Range
                overall_rating=4.3,
                ease_of_use_score=4.1,
                feature_score=4.7,
                value_for_money_score=3.8,
                design_rating=4.5,
                functionality_rating=4.6,
                value_rating=3.9,
                positive_sentiment_summary='Excellent cooking performance and precise temperature control',
                negative_sentiment_summary='High price point and complex features',
                key_insights='Professional-grade performance with precise control',
                common_complaints='Expensive, complex interface',
                standout_features='Precise temperature control, professional burners',
                total_reviews_analyzed=85
            ),
            AggregatedReview(
                luxury_appliance_id=2,  # Sub-Zero Refrigerator
                overall_rating=4.6,
                ease_of_use_score=4.4,
                feature_score=4.8,
                value_for_money_score=4.0,
                design_rating=4.7,
                functionality_rating=4.8,
                value_rating=4.1,
                positive_sentiment_summary='Whisper-quiet operation and excellent food preservation',
                negative_sentiment_summary='Expensive maintenance and slow ice maker',
                key_insights='Premium food preservation with quiet operation',
                common_complaints='Expensive repairs, slow ice maker',
                standout_features='Food preservation, quiet operation, built-in design',
                total_reviews_analyzed=92
            )
        ]
        
        # Add all reviews
        for review in ai_tool_reviews + appliance_reviews:
            db.session.add(review)
        
        db.session.commit()
        click.echo('Sample reviews seeded!')

if __name__ == '__main__':
    # Run with simpler settings to avoid hanging
    app.run(debug=False, host='127.0.0.1', port=5001, threaded=True) 