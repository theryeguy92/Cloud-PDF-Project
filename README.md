# AWS Kubernetes and Microservices Project
## Project Overview
This project demonstrates how to set up a distributed system using Kubernetes, Docker, Kafka, Machine Learning, and MySQL, hosted on AWS virtual machines (VMs). The system is designed to handle PDF uploads, process and summarize the content using an AI model, and store the metadata in a database.

## System Architecture
The project is hosted on four AWS VMs, each assigned a specific role:

# VM	# Role	                                # Details
VM1	    Kubernetes Master and PDF Upload API	Handles API requests, manages workloads, and coordinates Kubernetes cluster.
VM2	    Kafka and Zookeeper	                    Manages communication between services via Kafka messaging system.
VM3	    Machine Learning and Query Handler	    Processes PDFs and generates summaries using an AI model (e.g., LLaMA 2).
VM4	    MySQL Database	                        Stores processed data, metadata, and service logs.

## Technologies Used
AWS: Virtual machines to host the services.
Ansible: Automates deployment and configuration of VMs.
Kubernetes: Orchestrates containerized services.
Docker: Runs services in isolated containers.
Kafka: Message broker for inter-service communication.
Zookeeper: Coordinates Kafka instances.
Python: For API development and data processing.
FastAPI: Web framework for PDF upload and query APIs.
MySQL: Relational database for storing metadata.
LLaMA 2: Large language model for document summarization.

## Features

### PDF Upload and Processing:
Users upload PDFs via an API hosted on VM1.
PDF content is extracted, summarized, and sent to the database.
### Messaging System:
Kafka (on VM2) handles communication between services for PDF uploads, summaries, and database updates.
### Machine Learning:
VM3 hosts a containerized LLaMA 2 model to process and summarize PDFs.
Data Storage:
MySQL (on VM4) stores the processed data and metadata for querying.

## Project Setup
1. Infrastructure Setup
Ensure four VMs are running on AWS with the following IPs:

VM Name	Public IP	    Role
vm1	    3.22.250.2	    Kubernetes Master
vm2	    3.22.181.60	    Kafka & Zookeeper
vm3	    3.144.14.68	    Machine Learning Processing
vm4	    3.142.40.244	MySQL Database

## How the System Works
Step 1: PDF Upload API (VM1)
Users upload a PDF using the FastAPI web service.
PDF content is extracted using Python libraries (pdfplumber) and sent to VM3 via Kafka.
Step 2: Kafka Communication (VM2)
Kafka manages messages between services (e.g., PDF upload notifications, summaries).
Zookeeper ensures Kafka's reliability and consistency.
Step 3: Machine Learning Processing (VM3)
The PDF content is processed by a containerized LLaMA 2 model.
A summary is generated and sent to VM4 for storage.
Step 4: Data Storage (VM4)
Processed data and metadata are stored in a MySQL database.
Users can query the database for summaries or metadata via the API.

## Future Enhancements
Add Monitoring: Use Prometheus and Grafana for real-time system monitoring.
Enhance Security: Implement HTTPS and RBAC for Kubernetes services.
Scalability: Configure auto-scaling for Kubernetes workloads.

## Contributing
Fork the repository.
Create a new branch (git checkout -b feature-name).
Commit your changes (git commit -m "Add feature").
Push to the branch (git push origin feature-name).
Open a pull request.

## License
This project is licensed under the MIT License.