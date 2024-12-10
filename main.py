from fastapi import FastAPI, UploadFile, File, HTTPException
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Text
from sqlalchemy.orm import sessionmaker
from kafka import KafkaProducer, KafkaConsumer
from PyPDF2 import PdfReader
import json
import shutil
import os
from datetime import datetime

# FastAPI Instance
app = FastAPI()

# Database Connection
DATABASE_URL = "mysql+mysqlconnector://admin:password@172.31.1.75/pdf_rag_app"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define Tables
pdf_files = Table(
    "pdf_files", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("file_name", String(255), nullable=False),
    Column("upload_date", String(255), nullable=False),
    Column("context", Text, nullable=True),
)

metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Kafka Configuration
KAFKA_BROKER_URL = "172.31.9.51:9092"
PDF_UPLOAD_TOPIC = "pdf-upload"
USER_QUESTIONS_TOPIC = "user-questions"
LLM_RESPONSES_TOPIC = "llm-responses"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Function to parse PDF
def parse_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return None

# Endpoint to Upload PDF
@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse the PDF
    context = parse_pdf(file_location)

    # Create Kafka message
    message = {
        "file_name": file.filename,
        "upload_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "context": context,
    }

    # Publish to Kafka
    producer.send(PDF_UPLOAD_TOPIC, message)
    producer.flush()

    # Save metadata to database
    with SessionLocal() as session:
        session.execute(pdf_files.insert().values(
            file_name=file.filename,
            upload_date=message["upload_date"],
            context=context
        ))
        session.commit()

    return {"status": "File uploaded successfully", "file_name": file.filename}

# Endpoint for Chatbot Interaction
@app.post("/chatbot/")
async def chatbot(query: dict):
    user_query = query.get("query")
    if not user_query:
        raise HTTPException(status_code=400, detail="Query is required")

    # Publish user query to Kafka
    query_message = {"query": user_query}
    producer.send(USER_QUESTIONS_TOPIC, query_message)
    producer.flush()

    # Consume LLM response from Kafka
    consumer = KafkaConsumer(
        LLM_RESPONSES_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        auto_offset_reset="earliest",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    for message in consumer:
        response = message.value
        consumer.close()
        return {"answer": response.get("answer")}

