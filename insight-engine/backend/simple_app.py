from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///insight_engine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Simple model
class AITool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200))
    short_description = db.Column(db.Text)
    pricing_model = db.Column(db.String(50))
    primary_use_case = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'website': self.website,
            'short_description': self.short_description,
            'pricing_model': self.pricing_model,
            'primary_use_case': self.primary_use_case
        }

@app.route('/api/test')
def test():
    return jsonify({'message': 'Test route works!'})

@app.route('/api/ai-tools')
def get_ai_tools():
    try:
        tools = AITool.query.all()
        tools_data = [tool.to_dict() for tool in tools]
        
        return jsonify({
            'success': True,
            'data': tools_data,
            'count': len(tools_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5004) 