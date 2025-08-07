#!/usr/bin/env python3
"""
Database initialization script for the Insight Engine
Creates all tables and populates them with dummy data
"""

import os
import sys
from datetime import datetime, date
from decimal import Decimal

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

from project import create_app, db
from project.models.models import (
    Category, SubCategory, Product, ProductAttribute, 
    PriceHistory, AggregatedReview
)


def init_database():
    """Initialize the database with tables and dummy data"""
    
    # Create Flask app
    app = create_app('development')
    
    with app.app_context():
        print("🗃️  Dropping existing tables...")
        db.drop_all()
        
        print("🏗️  Creating new tables...")
        db.create_all()
        
        print("📊 Populating with dummy data...")
        
        # Create Categories from the original CategorySlider structure
        categories_data = [
            {
                'name': 'Technology',
                'description': 'AI tools, productivity software, and creative applications',
                'icon_svg': '<svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>',
                'status': 'Live',
                'display_order': 1
            },
            {
                'name': 'Appliances',
                'description': 'Kitchen, laundry, and luxury home appliances',
                'icon_svg': '<svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" /></svg>',
                'status': 'Live',
                'display_order': 2
            },
            {
                'name': 'Music',
                'description': 'Musical instruments and audio equipment',
                'icon_svg': '<svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" /></svg>',
                'status': 'Coming Soon',
                'display_order': 3
            },
            {
                'name': 'Transport',
                'description': 'Electric vehicles and personal transportation',
                'icon_svg': '<svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>',
                'status': 'Coming Soon',
                'display_order': 4
            },
            {
                'name': 'Gaming',
                'description': 'Gaming PCs, consoles, and accessories',
                'icon_svg': '<svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" /></svg>',
                'status': 'Coming Soon',
                'display_order': 5
            },
            {
                'name': 'Tech Products',
                'description': 'Pocket tech, desk accessories, and cool gadgets',
                'icon_svg': '<svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>',
                'status': 'Coming Soon',
                'display_order': 6
            },
            {
                'name': 'Fitness',
                'description': 'Home gym equipment, wearables, and outdoor gear',
                'icon_svg': '<svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>',
                'status': 'New',
                'display_order': 7
            }
        ]

        # Create category objects
        created_categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            created_categories.append(category)
        
        tech_category = created_categories[0]  # Technology
        appliances_category = created_categories[1]  # Appliances
        music_category = created_categories[2]  # Music
        transport_category = created_categories[3]  # Transport
        gaming_category = created_categories[4]  # Gaming
        tech_products_category = created_categories[5]  # Tech Products
        fitness_category = created_categories[6]  # Fitness
        
        db.session.add_all(created_categories)
        db.session.commit()
        
        # Create SubCategories from the original CategorySlider structure
        subcategories_data = [
            # Technology subcategories
            {'name': 'AI Tools', 'description': 'AI-powered software and applications', 'category_id': tech_category.id, 'status': 'Live', 'display_order': 1},
            {'name': 'Productivity', 'description': 'Productivity software and tools', 'category_id': tech_category.id, 'status': 'Coming Soon', 'display_order': 2},
            {'name': 'Creative', 'description': 'Creative software and design tools', 'category_id': tech_category.id, 'status': 'Coming Soon', 'display_order': 3},
            
            # Appliances subcategories
            {'name': 'Kitchen', 'description': 'Kitchen appliances and equipment', 'category_id': appliances_category.id, 'status': 'Coming Soon', 'display_order': 1},
            {'name': 'Laundry', 'description': 'Washing machines and dryers', 'category_id': appliances_category.id, 'status': 'Coming Soon', 'display_order': 2},
            {'name': 'Small Appliances', 'description': 'Countertop and small home appliances', 'category_id': appliances_category.id, 'status': 'Coming Soon', 'display_order': 3},
            {'name': 'Luxury Appliances', 'description': 'High-end kitchen and home appliances', 'category_id': appliances_category.id, 'status': 'Live', 'display_order': 4},
            
            # Music subcategories
            {'name': 'Guitars', 'description': 'Electric and acoustic guitars', 'category_id': music_category.id, 'status': 'Coming Soon', 'display_order': 1},
            {'name': 'Keyboards', 'description': 'Digital pianos and synthesizers', 'category_id': music_category.id, 'status': 'Coming Soon', 'display_order': 2},
            {'name': 'Turntables', 'description': 'DJ turntables and record players', 'category_id': music_category.id, 'status': 'Coming Soon', 'display_order': 3},
            {'name': 'Audio Gear', 'description': 'Audio equipment and accessories', 'category_id': music_category.id, 'status': 'Coming Soon', 'display_order': 4},
            
            # Transport subcategories
            {'name': 'Scooters', 'description': 'Electric scooters and e-mobility', 'category_id': transport_category.id, 'status': 'Coming Soon', 'display_order': 1},
            {'name': 'Electric Skateboards', 'description': 'Electric longboards and skateboards', 'category_id': transport_category.id, 'status': 'Coming Soon', 'display_order': 2},
            {'name': 'E-Bikes', 'description': 'Electric bicycles and e-bike accessories', 'category_id': transport_category.id, 'status': 'Coming Soon', 'display_order': 3},
            {'name': 'Electric Cars', 'description': 'Electric vehicles and EV accessories', 'category_id': transport_category.id, 'status': 'Coming Soon', 'display_order': 4},
            
            # Gaming subcategories
            {'name': 'Gaming PCs', 'description': 'Pre-built and custom gaming computers', 'category_id': gaming_category.id, 'status': 'Coming Soon', 'display_order': 1},
            {'name': 'Consoles', 'description': 'Gaming consoles and accessories', 'category_id': gaming_category.id, 'status': 'Coming Soon', 'display_order': 2},
            {'name': 'Peripherals', 'description': 'Gaming keyboards, mice, and headsets', 'category_id': gaming_category.id, 'status': 'Coming Soon', 'display_order': 3},
            {'name': 'Mobile Gaming', 'description': 'Mobile gaming accessories and controllers', 'category_id': gaming_category.id, 'status': 'Coming Soon', 'display_order': 4},
            
            # Tech Products subcategories
            {'name': 'Pocket Tech', 'description': 'Portable gadgets and pocket devices', 'category_id': tech_products_category.id, 'status': 'Coming Soon', 'display_order': 1},
            {'name': 'Desk Tech', 'description': 'Desktop accessories and workspace tech', 'category_id': tech_products_category.id, 'status': 'Coming Soon', 'display_order': 2},
            {'name': 'Tech Toys', 'description': 'Fun tech gadgets and electronic toys', 'category_id': tech_products_category.id, 'status': 'Coming Soon', 'display_order': 3},
            {'name': 'Cool Gadgets', 'description': 'Unique and innovative tech products', 'category_id': tech_products_category.id, 'status': 'Coming Soon', 'display_order': 4},
            
            # Fitness subcategories
            {'name': 'Home Gym', 'description': 'Home gym equipment and fitness machines', 'category_id': fitness_category.id, 'status': 'New', 'display_order': 1},
            {'name': 'Wearables', 'description': 'Fitness trackers and smart watches', 'category_id': fitness_category.id, 'status': 'New', 'display_order': 2},
            {'name': 'Supplements', 'description': 'Fitness supplements and nutrition', 'category_id': fitness_category.id, 'status': 'New', 'display_order': 3},
            {'name': 'Outdoor Gear', 'description': 'Outdoor fitness and sports equipment', 'category_id': fitness_category.id, 'status': 'New', 'display_order': 4},
        ]

        # Create subcategory objects
        created_subcategories = []
        for subcat_data in subcategories_data:
            subcategory = SubCategory(**subcat_data)
            created_subcategories.append(subcategory)
        
        # Get specific subcategories for products
        ai_tools_subcategory = created_subcategories[0]  # AI Tools
        luxury_appliances_subcategory = created_subcategories[6]  # Luxury Appliances
        
        db.session.add_all(created_subcategories)
        db.session.commit()
        
        # Create AI Tools Products
        ai_products_data = [
            {
                'name': 'Notion AI',
                'brand': 'Notion Labs',
                'short_description': 'AI-powered workspace that helps you write, plan, and get organized.',
                'insight_snippet': 'Excellent for content creation and note-taking, but can be slow with large databases. Users love the seamless integration with existing Notion workflows.',
                'image_url': 'https://example.com/notion-ai.png',
                'attributes': [
                    {'key': 'Pricing Model', 'value': 'Freemium'},
                    {'key': 'Primary Use Case', 'value': 'Content Creation'},
                    {'key': 'Integration', 'value': 'Native Notion'},
                    {'key': 'Languages Supported', 'value': 'English, Spanish, French, German'}
                ],
                'price_history': [
                    {'price': 0.0, 'retailer_name': 'Notion (Free Plan)', 'date_recorded': date(2024, 1, 1)},
                    {'price': 8.0, 'retailer_name': 'Notion (Plus Plan)', 'date_recorded': date(2024, 1, 1)},
                    {'price': 15.0, 'retailer_name': 'Notion (Business Plan)', 'date_recorded': date(2024, 1, 1)}
                ],
                'review': {
                    'overall_rating': 4.2,
                    'ease_of_use_score': 4.0,
                    'feature_score': 4.5,
                    'value_for_money_score': 4.1,
                    'design_rating': 4.6,
                    'functionality_rating': 4.3,
                    'reliability_rating': 3.8,
                    'positive_sentiment_summary': 'Users praise the seamless integration with Notion and powerful content generation capabilities.',
                    'negative_sentiment_summary': 'Some users report slower performance with large databases and occasional AI hallucinations.',
                    'key_insights': 'Best for teams already using Notion; excellent for brainstorming and content drafts.',
                    'common_complaints': 'Performance issues, limited customization options',
                    'standout_features': 'Native Notion integration, contextual AI assistance',
                    'total_reviews_analyzed': 1247
                }
            },
            {
                'name': 'ChatGPT Plus',
                'brand': 'OpenAI',
                'short_description': 'Advanced conversational AI with GPT-4 access and priority response times.',
                'insight_snippet': 'The gold standard for conversational AI. Excellent reasoning capabilities but can be verbose. Users appreciate the reliability and consistent quality.',
                'image_url': 'https://example.com/chatgpt-plus.png',
                'attributes': [
                    {'key': 'Pricing Model', 'value': 'Subscription'},
                    {'key': 'Primary Use Case', 'value': 'General AI Assistant'},
                    {'key': 'Model Version', 'value': 'GPT-4'},
                    {'key': 'Monthly Limit', 'value': '40 messages per 3 hours'}
                ],
                'price_history': [
                    {'price': 20.0, 'retailer_name': 'OpenAI', 'date_recorded': date(2024, 1, 1)},
                    {'price': 20.0, 'retailer_name': 'OpenAI', 'date_recorded': date(2024, 6, 1)}
                ],
                'review': {
                    'overall_rating': 4.6,
                    'ease_of_use_score': 4.8,
                    'feature_score': 4.7,
                    'value_for_money_score': 4.2,
                    'design_rating': 4.5,
                    'functionality_rating': 4.8,
                    'reliability_rating': 4.4,
                    'positive_sentiment_summary': 'Users love the consistent quality, reasoning capabilities, and reliable performance.',
                    'negative_sentiment_summary': 'Some users find it verbose and wish for more customization options.',
                    'key_insights': 'Best overall AI assistant for general use; excellent for complex reasoning tasks.',
                    'common_complaints': 'Verbose responses, usage limits',
                    'standout_features': 'Superior reasoning, consistent quality, reliable uptime',
                    'total_reviews_analyzed': 3421
                }
            },
            {
                'name': 'Claude Pro',
                'brand': 'Anthropic',
                'short_description': 'Constitutional AI assistant focused on being helpful, harmless, and honest.',
                'insight_snippet': 'Excellent for analysis and writing tasks. Users appreciate the thoughtful responses and safety focus, though it can be overly cautious at times.',
                'image_url': 'https://example.com/claude-pro.png',
                'attributes': [
                    {'key': 'Pricing Model', 'value': 'Subscription'},
                    {'key': 'Primary Use Case', 'value': 'Analysis & Writing'},
                    {'key': 'Context Window', 'value': '100k tokens'},
                    {'key': 'Safety Focus', 'value': 'High'}
                ],
                'price_history': [
                    {'price': 20.0, 'retailer_name': 'Anthropic', 'date_recorded': date(2024, 3, 1)},
                    {'price': 20.0, 'retailer_name': 'Anthropic', 'date_recorded': date(2024, 6, 1)}
                ],
                'review': {
                    'overall_rating': 4.4,
                    'ease_of_use_score': 4.3,
                    'feature_score': 4.2,
                    'value_for_money_score': 4.1,
                    'design_rating': 4.0,
                    'functionality_rating': 4.5,
                    'reliability_rating': 4.3,
                    'positive_sentiment_summary': 'Users appreciate the thoughtful, nuanced responses and strong safety measures.',
                    'negative_sentiment_summary': 'Some users find it overly cautious and wish it was more creative.',
                    'key_insights': 'Best for analytical tasks and professional writing; excellent safety record.',
                    'common_complaints': 'Overly cautious, less creative than competitors',
                    'standout_features': 'Large context window, thoughtful responses, strong safety',
                    'total_reviews_analyzed': 892
                }
            },
            {
                'name': 'Midjourney',
                'brand': 'Midjourney Inc',
                'short_description': 'AI image generation tool known for artistic and creative outputs.',
                'insight_snippet': 'The go-to choice for artistic AI image generation. Produces stunning visuals but requires Discord and has a learning curve for prompting.',
                'image_url': 'https://example.com/midjourney.png',
                'attributes': [
                    {'key': 'Pricing Model', 'value': 'Subscription'},
                    {'key': 'Primary Use Case', 'value': 'Image Generation'},
                    {'key': 'Platform', 'value': 'Discord Bot'},
                    {'key': 'Art Style', 'value': 'Artistic/Creative'}
                ],
                'price_history': [
                    {'price': 10.0, 'retailer_name': 'Midjourney (Basic)', 'date_recorded': date(2024, 1, 1)},
                    {'price': 30.0, 'retailer_name': 'Midjourney (Standard)', 'date_recorded': date(2024, 1, 1)},
                    {'price': 60.0, 'retailer_name': 'Midjourney (Pro)', 'date_recorded': date(2024, 1, 1)}
                ],
                'review': {
                    'overall_rating': 4.5,
                    'ease_of_use_score': 3.7,
                    'feature_score': 4.8,
                    'value_for_money_score': 4.0,
                    'design_rating': 4.9,
                    'functionality_rating': 4.6,
                    'reliability_rating': 4.2,
                    'positive_sentiment_summary': 'Users love the artistic quality and unique aesthetic of generated images.',
                    'negative_sentiment_summary': 'Discord interface can be confusing, and prompting requires practice.',
                    'key_insights': 'Best for artistic and creative image generation; steep learning curve but amazing results.',
                    'common_complaints': 'Discord interface, learning curve, waiting times',
                    'standout_features': 'Artistic quality, unique aesthetic, community aspect',
                    'total_reviews_analyzed': 2156
                }
            }
        ]
        
        # Create Luxury Appliances Products
        appliance_products_data = [
            {
                'name': 'Dacor DRF487500AP 48" Built-In French Door Refrigerator',
                'brand': 'Dacor',
                'short_description': 'Professional-grade 48" French door refrigerator with advanced cooling technology.',
                'insight_snippet': 'Praised for its whisper-quiet operation and precise temperature control, but owners note the ice maker can be slow and the price is steep.',
                'image_url': 'https://example.com/dacor-fridge.png',
                'attributes': [
                    {'key': 'MSRP', 'value': '14449'},
                    {'key': 'Style Tags', 'value': 'Modern, Professional-Grade, Sleek'},
                    {'key': 'Capacity', 'value': '26.6 cu. ft.'},
                    {'key': 'Energy Star', 'value': 'Yes'},
                    {'key': 'Finish Options', 'value': 'Stainless Steel, Panel Ready'},
                    {'key': 'Warranty', 'value': '2 years full, 12 years sealed system'}
                ],
                'price_history': [
                    {'price': 14449.0, 'retailer_name': 'Dacor Official', 'date_recorded': date(2024, 1, 1)},
                    {'price': 13999.0, 'retailer_name': 'Home Depot', 'date_recorded': date(2024, 3, 1)},
                    {'price': 14200.0, 'retailer_name': 'Lowes', 'date_recorded': date(2024, 3, 1)}
                ],
                'review': {
                    'overall_rating': 4.3,
                    'ease_of_use_score': 4.1,
                    'feature_score': 4.6,
                    'value_for_money_score': 3.8,
                    'design_rating': 4.7,
                    'functionality_rating': 4.4,
                    'reliability_rating': 4.2,
                    'positive_sentiment_summary': 'Owners love the quiet operation, precise temperature control, and sleek design.',
                    'negative_sentiment_summary': 'High price point and slow ice maker are common complaints.',
                    'key_insights': 'Excellent choice for serious home chefs who value precision and quiet operation.',
                    'common_complaints': 'High price, slow ice maker, complex controls',
                    'standout_features': 'Whisper-quiet operation, precise temperature zones, premium build quality',
                    'total_reviews_analyzed': 127
                }
            },
            {
                'name': 'Wolf SO30CE/S/PH 30" E Series Contemporary Convection Steam Oven',
                'brand': 'Wolf',
                'short_description': 'Professional convection steam oven with precise temperature and humidity control.',
                'insight_snippet': 'A chef\'s dream with incredible versatility and precision. Users rave about the cooking results but note the steep learning curve and premium price.',
                'image_url': 'https://example.com/wolf-oven.png',
                'attributes': [
                    {'key': 'MSRP', 'value': '8495'},
                    {'key': 'Style Tags', 'value': 'Contemporary, Professional, Premium'},
                    {'key': 'Capacity', 'value': '1.8 cu. ft.'},
                    {'key': 'Power', 'value': '240V'},
                    {'key': 'Installation', 'value': 'Built-in'},
                    {'key': 'Warranty', 'value': '2 years full parts and labor'}
                ],
                'price_history': [
                    {'price': 8495.0, 'retailer_name': 'Wolf Official', 'date_recorded': date(2024, 1, 1)},
                    {'price': 8295.0, 'retailer_name': 'AJ Madison', 'date_recorded': date(2024, 2, 1)},
                    {'price': 8399.0, 'retailer_name': 'Yale Appliance', 'date_recorded': date(2024, 3, 1)}
                ],
                'review': {
                    'overall_rating': 4.6,
                    'ease_of_use_score': 3.9,
                    'feature_score': 4.8,
                    'value_for_money_score': 3.7,
                    'design_rating': 4.8,
                    'functionality_rating': 4.9,
                    'reliability_rating': 4.5,
                    'positive_sentiment_summary': 'Professional chefs and serious home cooks love the precision and versatility.',
                    'negative_sentiment_summary': 'Steep learning curve and high price are the main drawbacks.',
                    'key_insights': 'Best for serious cooks who want restaurant-quality results at home.',
                    'common_complaints': 'Complex operation, high price, requires learning',
                    'standout_features': 'Precise steam control, professional results, versatile cooking modes',
                    'total_reviews_analyzed': 89
                }
            },
            {
                'name': 'Miele G7366SCVi AutoDos Fully Integrated Dishwasher',
                'brand': 'Miele',
                'short_description': 'Ultra-quiet fully integrated dishwasher with automatic detergent dispensing.',
                'insight_snippet': 'The quietest dishwasher on the market with excellent cleaning performance. Users love the AutoDos feature but find the controls overly complex.',
                'image_url': 'https://example.com/miele-dishwasher.png',
                'attributes': [
                    {'key': 'MSRP', 'value': '2799'},
                    {'key': 'Style Tags', 'value': 'Modern, Quiet, Efficient'},
                    {'key': 'Noise Level', 'value': '38 dBA'},
                    {'key': 'Capacity', 'value': '16 place settings'},
                    {'key': 'Energy Star', 'value': 'Yes'},
                    {'key': 'Warranty', 'value': '2 years full'}
                ],
                'price_history': [
                    {'price': 2799.0, 'retailer_name': 'Miele Official', 'date_recorded': date(2024, 1, 1)},
                    {'price': 2699.0, 'retailer_name': 'AJ Madison', 'date_recorded': date(2024, 2, 15)},
                    {'price': 2750.0, 'retailer_name': 'Home Depot', 'date_recorded': date(2024, 3, 1)}
                ],
                'review': {
                    'overall_rating': 4.5,
                    'ease_of_use_score': 3.8,
                    'feature_score': 4.7,
                    'value_for_money_score': 4.0,
                    'design_rating': 4.6,
                    'functionality_rating': 4.8,
                    'reliability_rating': 4.7,
                    'positive_sentiment_summary': 'Users love the ultra-quiet operation, excellent cleaning, and AutoDos convenience.',
                    'negative_sentiment_summary': 'Complex controls and high price are the main concerns.',
                    'key_insights': 'Perfect for open-concept homes where noise is a concern; excellent German engineering.',
                    'common_complaints': 'Complex controls, high price, long cycle times',
                    'standout_features': 'Ultra-quiet operation, AutoDos detergent dispensing, excellent cleaning',
                    'total_reviews_analyzed': 203
                }
            },
            {
                'name': 'Thermador PRD486WDG 48" Pro Grand Gas Range',
                'brand': 'Thermador',
                'short_description': 'Professional 48" gas range with 6 burners and griddle for serious home cooking.',
                'insight_snippet': 'A powerhouse range that delivers restaurant-quality performance. Users love the cooking power but note it requires professional installation and adequate ventilation.',
                'image_url': 'https://example.com/thermador-range.png',
                'attributes': [
                    {'key': 'MSRP', 'value': '12999'},
                    {'key': 'Style Tags', 'value': 'Professional, Powerful, Premium'},
                    {'key': 'Fuel Type', 'value': 'Natural Gas / Propane'},
                    {'key': 'Burner Count', 'value': '6 + Griddle'},
                    {'key': 'Oven Capacity', 'value': '5.1 cu. ft.'},
                    {'key': 'Warranty', 'value': '2 years full parts and labor'}
                ],
                'price_history': [
                    {'price': 12999.0, 'retailer_name': 'Thermador Official', 'date_recorded': date(2024, 1, 1)},
                    {'price': 12599.0, 'retailer_name': 'Yale Appliance', 'date_recorded': date(2024, 2, 1)},
                    {'price': 12799.0, 'retailer_name': 'AJ Madison', 'date_recorded': date(2024, 3, 1)}
                ],
                'review': {
                    'overall_rating': 4.4,
                    'ease_of_use_score': 4.2,
                    'feature_score': 4.7,
                    'value_for_money_score': 3.9,
                    'design_rating': 4.6,
                    'functionality_rating': 4.8,
                    'reliability_rating': 4.1,
                    'positive_sentiment_summary': 'Home chefs love the power, versatility, and professional-grade performance.',
                    'negative_sentiment_summary': 'Requires professional installation and generates significant heat.',
                    'key_insights': 'Ideal for serious home cooks who want restaurant-quality equipment.',
                    'common_complaints': 'High heat output, requires professional installation, expensive',
                    'standout_features': 'Powerful burners, griddle option, professional performance',
                    'total_reviews_analyzed': 156
                }
            }
        ]
        
        # Add AI Tools products
        for product_data in ai_products_data:
            product = Product(
                name=product_data['name'],
                brand=product_data['brand'],
                short_description=product_data['short_description'],
                insight_snippet=product_data['insight_snippet'],
                image_url=product_data['image_url'],
                subcategory_id=ai_tools_subcategory.id
            )
            db.session.add(product)
            db.session.flush()  # Get the product ID
            
            # Add attributes
            for attr_data in product_data['attributes']:
                attribute = ProductAttribute(
                    key=attr_data['key'],
                    value=attr_data['value'],
                    product_id=product.id
                )
                db.session.add(attribute)
            
            # Add price history
            for price_data in product_data['price_history']:
                price = PriceHistory(
                    price=price_data['price'],
                    retailer_name=price_data['retailer_name'],
                    date_recorded=price_data['date_recorded'],
                    product_id=product.id
                )
                db.session.add(price)
            
            # Add review
            review_data = product_data['review']
            review = AggregatedReview(
                product_id=product.id,
                overall_rating=review_data['overall_rating'],
                ease_of_use_score=review_data['ease_of_use_score'],
                feature_score=review_data['feature_score'],
                value_for_money_score=review_data['value_for_money_score'],
                design_rating=review_data['design_rating'],
                functionality_rating=review_data['functionality_rating'],
                reliability_rating=review_data['reliability_rating'],
                positive_sentiment_summary=review_data['positive_sentiment_summary'],
                negative_sentiment_summary=review_data['negative_sentiment_summary'],
                key_insights=review_data['key_insights'],
                common_complaints=review_data['common_complaints'],
                standout_features=review_data['standout_features'],
                total_reviews_analyzed=review_data['total_reviews_analyzed']
            )
            db.session.add(review)
        
        # Add Luxury Appliances products
        for product_data in appliance_products_data:
            product = Product(
                name=product_data['name'],
                brand=product_data['brand'],
                short_description=product_data['short_description'],
                insight_snippet=product_data['insight_snippet'],
                image_url=product_data['image_url'],
                subcategory_id=luxury_appliances_subcategory.id
            )
            db.session.add(product)
            db.session.flush()  # Get the product ID
            
            # Add attributes
            for attr_data in product_data['attributes']:
                attribute = ProductAttribute(
                    key=attr_data['key'],
                    value=attr_data['value'],
                    product_id=product.id
                )
                db.session.add(attribute)
            
            # Add price history
            for price_data in product_data['price_history']:
                price = PriceHistory(
                    price=price_data['price'],
                    retailer_name=price_data['retailer_name'],
                    date_recorded=price_data['date_recorded'],
                    product_id=product.id
                )
                db.session.add(price)
            
            # Add review
            review_data = product_data['review']
            review = AggregatedReview(
                product_id=product.id,
                overall_rating=review_data['overall_rating'],
                ease_of_use_score=review_data['ease_of_use_score'],
                feature_score=review_data['feature_score'],
                value_for_money_score=review_data['value_for_money_score'],
                design_rating=review_data['design_rating'],
                functionality_rating=review_data['functionality_rating'],
                reliability_rating=review_data['reliability_rating'],
                positive_sentiment_summary=review_data['positive_sentiment_summary'],
                negative_sentiment_summary=review_data['negative_sentiment_summary'],
                key_insights=review_data['key_insights'],
                common_complaints=review_data['common_complaints'],
                standout_features=review_data['standout_features'],
                total_reviews_analyzed=review_data['total_reviews_analyzed']
            )
            db.session.add(review)
        
        # Commit all changes
        db.session.commit()
        
        print("✅ Database initialization completed successfully!")
        print(f"📊 Created:")
        print(f"   • {len(categories_data)} categories (Technology, Appliances, Music, Transport, Gaming, Tech Products, Fitness)")
        print(f"   • {len(subcategories_data)} subcategories from original CategorySlider")
        print(f"   • {len(ai_products_data + appliance_products_data)} products")
        print(f"   • {sum(len(p['attributes']) for p in ai_products_data + appliance_products_data)} product attributes")
        print(f"   • {sum(len(p['price_history']) for p in ai_products_data + appliance_products_data)} price history entries")
        print(f"   • {len(ai_products_data + appliance_products_data)} aggregated reviews")
        print(f"   • Category statuses: 2 Live, 4 Coming Soon, 1 New")
        print(f"   • Only AI Tools and Luxury Appliances have products (Live status)")


if __name__ == '__main__':
    init_database()