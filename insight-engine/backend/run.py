from app import create_app, db
from app.models.ai_tool import AITool
from app.models.aggregated_review import AggregatedReview
from app.models.luxe_appliance import LuxeAppliance
from app.models.luxe_review import LuxeReview
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
    """Seed the database with sample AI tools."""
    with app.app_context():
        # Clear existing data
        AggregatedReview.query.delete()
        AITool.query.delete()
        
        # Sample AI tools
        tools = [
            AITool(
                name='ChatGPT',
                website='https://chat.openai.com',
                short_description='Advanced language model for conversation and text generation',
                pricing_model='Freemium',
                primary_use_case='Content Creation'
            ),
            AITool(
                name='Midjourney',
                website='https://midjourney.com',
                short_description='AI-powered image generation from text descriptions',
                pricing_model='Subscription',
                primary_use_case='Image Generation'
            ),
            AITool(
                name='Jasper',
                website='https://jasper.ai',
                short_description='AI writing assistant for marketing and content creation',
                pricing_model='Subscription',
                primary_use_case='Content Creation'
            ),
            AITool(
                name='Notion AI',
                website='https://notion.so',
                short_description='AI-powered workspace for notes, docs, and collaboration',
                pricing_model='Freemium',
                primary_use_case='Productivity'
            ),
            AITool(
                name='Copy.ai',
                website='https://copy.ai',
                short_description='AI copywriting tool for marketing and sales content',
                pricing_model='Freemium',
                primary_use_case='Content Creation'
            )
        ]
        
        for tool in tools:
            db.session.add(tool)
        
        db.session.commit()
        click.echo('AI tools seeded!')

@app.cli.command('seed-luxe-appliances')
def seed_luxe_appliances():
    """Seed the database with luxury appliance brands and models."""
    with app.app_context():
        # Clear existing data
        LuxeReview.query.delete()
        LuxeAppliance.query.delete()
        
        # Sample luxury appliances
        appliances = [
            # Dacor (Main brand)
            LuxeAppliance(
                name='Dacor 48" Professional Range',
                brand='Dacor',
                category='Range',
                model_number='DR48SGP',
                price_range='$8,000-$12,000',
                website='https://dacor.com',
                description='Professional-grade dual fuel range with 6 burners and convection oven',
                features='Dual fuel, 6 burners, convection oven, steam cooking, WiFi connectivity',
                design_style='Modern',
                finish_options='Stainless steel, matte black, panel ready',
                dimensions='48" W x 30" D x 36" H',
                energy_rating='Energy Star certified',
                warranty='2-year limited warranty'
            ),
            LuxeAppliance(
                name='Dacor 36" French Door Refrigerator',
                brand='Dacor',
                category='Refrigerator',
                model_number='DR36FD',
                price_range='$6,000-$9,000',
                website='https://dacor.com',
                description='Premium French door refrigerator with advanced cooling technology',
                features='French doors, dual cooling, humidity control, ice maker, WiFi',
                design_style='Modern',
                finish_options='Stainless steel, panel ready',
                dimensions='36" W x 30" D x 70" H',
                energy_rating='Energy Star certified',
                warranty='2-year limited warranty'
            ),
            
            # Sub Zero/Wolf/Cove
            LuxeAppliance(
                name='Sub-Zero 48" Built-In Refrigerator',
                brand='Sub-Zero',
                category='Refrigerator',
                model_number='BI-48UFD/O',
                price_range='$15,000-$20,000',
                website='https://subzero-wolf.com',
                description='Premium built-in refrigerator with dual refrigeration system',
                features='Dual refrigeration, air purification, WiFi, panel ready',
                design_style='Modern',
                finish_options='Stainless steel, panel ready, custom panels',
                dimensions='48" W x 24" D x 84" H',
                energy_rating='Energy Star certified',
                warranty='2-year limited warranty'
            ),
            LuxeAppliance(
                name='Wolf 48" Dual Fuel Range',
                brand='Wolf',
                category='Range',
                model_number='DF486',
                price_range='$12,000-$16,000',
                website='https://subzero-wolf.com',
                description='Professional dual fuel range with 6 burners and infrared broiler',
                features='Dual fuel, 6 burners, infrared broiler, convection oven',
                design_style='Professional',
                finish_options='Stainless steel, black stainless',
                dimensions='48" W x 30" D x 36" H',
                energy_rating='Energy Star certified',
                warranty='2-year limited warranty'
            ),
            
            # Thermador
            LuxeAppliance(
                name='Thermador 48" Professional Range',
                brand='Thermador',
                category='Range',
                model_number='PRG486GG',
                price_range='$10,000-$14,000',
                website='https://thermador.com',
                description='Professional gas range with Star Burner technology',
                features='Star burners, convection oven, WiFi, steam cooking',
                design_style='Modern',
                finish_options='Stainless steel, black stainless',
                dimensions='48" W x 30" D x 36" H',
                energy_rating='Energy Star certified',
                warranty='2-year limited warranty'
            ),
            
            # Viking
            LuxeAppliance(
                name='Viking 48" Professional Range',
                brand='Viking',
                category='Range',
                model_number='VGR548',
                price_range='$9,000-$13,000',
                website='https://vikingrange.com',
                description='Professional gas range with commercial-grade performance',
                features='Commercial burners, convection oven, heavy-duty construction',
                design_style='Professional',
                finish_options='Stainless steel, black, white',
                dimensions='48" W x 30" D x 36" H',
                energy_rating='Energy Star certified',
                warranty='2-year limited warranty'
            ),
            
            # Fisher & Paykel
            LuxeAppliance(
                name='Fisher & Paykel 36" French Door Refrigerator',
                brand='Fisher & Paykel',
                category='Refrigerator',
                model_number='RF522W',
                price_range='$4,000-$6,000',
                website='https://fisherpaykel.com',
                description='Innovative French door refrigerator with ActiveSmart technology',
                features='ActiveSmart, dual cooling, ice maker, WiFi',
                design_style='Modern',
                finish_options='Stainless steel, panel ready',
                dimensions='36" W x 30" D x 70" H',
                energy_rating='Energy Star certified',
                warranty='2-year limited warranty'
            ),
            
            # Monogram
            LuxeAppliance(
                name='Monogram 48" Professional Range',
                brand='Monogram',
                category='Range',
                model_number='ZGP486N',
                price_range='$8,000-$12,000',
                website='https://monogram.com',
                description='Professional gas range with precision cooking technology',
                features='Precision cooking, convection oven, WiFi, steam cooking',
                design_style='Modern',
                finish_options='Stainless steel, black stainless',
                dimensions='48" W x 30" D x 36" H',
                energy_rating='Energy Star certified',
                warranty='2-year limited warranty'
            ),
            
            # SKS (Signature Kitchen Suite)
            LuxeAppliance(
                name='SKS 48" Professional Range',
                brand='SKS',
                category='Range',
                model_number='SRG486',
                price_range='$11,000-$15,000',
                website='https://signaturekitchensuite.com',
                description='Professional range with advanced cooking technology',
                features='Professional burners, convection oven, WiFi, steam cooking',
                design_style='Modern',
                finish_options='Stainless steel, panel ready',
                dimensions='48" W x 30" D x 36" H',
                energy_rating='Energy Star certified',
                warranty='2-year limited warranty'
            ),
            
            # JennAir
            LuxeAppliance(
                name='JennAir 48" Professional Range',
                brand='JennAir',
                category='Range',
                model_number='JGRP486',
                price_range='$7,000-$10,000',
                website='https://jennair.com',
                description='Professional range with advanced cooking features',
                features='Professional burners, convection oven, WiFi',
                design_style='Modern',
                finish_options='Stainless steel, black stainless',
                dimensions='48" W x 30" D x 36" H',
                energy_rating='Energy Star certified',
                warranty='2-year limited warranty'
            ),
            
            # Gaggenau
            LuxeAppliance(
                name='Gaggenau 48" Professional Range',
                brand='Gaggenau',
                category='Range',
                model_number='VK486',
                price_range='$18,000-$25,000',
                website='https://gaggenau.com',
                description='Ultra-premium professional range with precision engineering',
                features='Precision burners, convection oven, steam cooking, WiFi',
                design_style='Ultra-modern',
                finish_options='Stainless steel, panel ready, custom finishes',
                dimensions='48" W x 30" D x 36" H',
                energy_rating='Energy Star certified',
                warranty='2-year limited warranty'
            )
        ]
        
        for appliance in appliances:
            db.session.add(appliance)
        
        db.session.commit()
        click.echo('Luxury appliances seeded!')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 