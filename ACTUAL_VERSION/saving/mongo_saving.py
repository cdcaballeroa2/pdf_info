from pymongo import MongoClient

client = MongoClient("mongodb+srv://danepdf:dane_pdf@cluster0.js2al.mongodb.net/?retryWrites=true&w=majority")
db = client.dane_pdf
collection = db.aspirantes

def insert_to_bd(element: dict):
    x = collection.insert_one(element)