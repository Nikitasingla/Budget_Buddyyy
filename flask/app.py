# from flask import Flask, jsonify, request
# from flask_restful import Resource,Api
# from flask_sqlalchemy import SQLAlchemy


# app=Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///budgetbbb.db"
# app.config["SECRET_KEY"]="flasked"

# db=SQLAlchemy(app)
# api=Api(app)


# class stocks(db.Model):
#     __tablename__="stocks"



# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, request,jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocks.db'
db = SQLAlchemy(app)



class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    image_url = db.Column(db.String(300))  # ✅ New column for image/logo URL

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "price": self.price,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "image_url": self.image_url
        }
# sample_stocks = [
#     {
#         "id":1,
#         "symbol": "AAPLE",
#         "price": 185.25,
#         "open": 183.50,
#         "high": 186.30,
#         "low": 182.75,
#         "image_url": "https://logo.clearbit.com/apple.com"
#     },
#     {
#         "id":2,
#         "symbol": "GOOGLE",
#         "price": 2745.60,
#         "open": 2700.00,
#         "high": 2758.90,
#         "low": 2689.45,
#         "image_url": "https://logo.clearbit.com/google.com"
#     },
#     {
#         "id":3,
#         "symbol": "TESLA",
#         "price": 720.85,
#         "open": 710.10,
#         "high": 725.50,
#         "low": 705.30,
#         "image_url": "https://logo.clearbit.com/tesla.com"
#     },
#     {
#         "id":4,
#         "symbol": "MICROSOFT",
#         "price": 315.90,
#         "open": 310.75,
#         "high": 318.40,
#         "low": 309.20,
#         "image_url": "https://logo.clearbit.com/microsoft.com"
#     },
#     {
#         "id":5,
#         "symbol": "AMAZON",
#         "price": 135.70,
#         "open": 133.40,
#         "high": 136.90,
#         "low": 132.85,
#         "image_url": "https://logo.clearbit.com/amazon.com"
#     },
#     {
#         "id":6,
#         "symbol": "META",
#         "price": 330.45,
#         "open": 327.00,
#         "high": 333.25,
#         "low": 324.80,
#         "image_url": "https://logo.clearbit.com/meta.com"
#     }
# ]

# API resource
class StockAPI(Resource):
    def get(self, symbol=None):
        if symbol==None:
            data=Stock.query.all()
            return jsonify([stock.to_dict() for stock in data])
            # return jsonify(sample_stocks)
        stock=Stock.query.filter_by(symbol=symbol.upper()).first()
        if stock:
            return jsonify(stock.to_dict())
        return {"msg":"Stock Not Found"},404

    def post(self):
        data = request.get_json()
        existing = Stock.query.filter_by(symbol=data.get('symbol').upper()).first()
        if existing:
            return {"error": "Stock already exists"}, 400

        new_stock = Stock(
            symbol=data.get('symbol').upper(),
            price=data.get('price'),
            open=data.get('open'),
            high=data.get('high'),
            low=data.get('low'),
            image_url=data.get('image_url')  # ✅ Accept image_url in request
        )
        db.session.add(new_stock)
        db.session.commit()
        return new_stock.to_dict(), 201
    def put(self,symbol):
        data=request.get_json()
        find_product=Stock.query.filter_by(symbol=symbol.upper()).first()
        if find_product:
            find_product.symbol=data.get("symbol",find_product.symbol)
            find_product.price=data.get("price",find_product.price)
            find_product.open=data.get("open",find_product.open)
            find_product.high=data.get("high",find_product.high)
            find_product.low=data.get("low",find_product.low)
            find_product.image_url=data.get("image_url",find_product.image_url)
            db.session.commit()
            return{"msg":"Stock updated successfully"}
        else:
            return{"msg":"Stock Not found"},404
        
    def delete(self,symbol):
        product=Stock.query.filter_by(symbol=symbol.upper()).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            return {"msg":"Stock deleted successfully"}
        else:
            return{"msg":"Stock not Found"}
api.add_resource(StockAPI,"/api/stock/" ,"/api/stock/<string:symbol>")




# Create DB tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
