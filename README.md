
### **Improved README.md**

# **AWS Kubernetes and Microservices Project**

## **Overview**
This project demonstrates the deployment of a cloud-native distributed system hosted on AWS virtual machines (VMs). The system leverages Kubernetes for orchestration, Docker for containerization, Kafka for inter-service messaging, and LLaMA 2 for AI-based PDF summarization. It showcases how to manage and scale microservices in a cloud environment while processing, summarizing, and storing PDF content.

---

## **Architecture**

The project is hosted on four AWS VMs, each assigned specific roles to maintain modularity and scalability:

| **VM Name** | **Public IP**  | **Role**                       | **Responsibilities**                                           |
|-------------|----------------|--------------------------------|---------------------------------------------------------------|
| **vm1**     | `3.22.250.2`   | Kubernetes Master & API        | Hosts API for PDF uploads, coordinates workloads, manages cluster. |
| **vm2**     | `3.22.181.60`  | Kafka & Zookeeper             | Manages communication using Kafka, coordinates Kafka with Zookeeper. |
| **vm3**     | `3.144.14.68`  | Machine Learning & Query API  | Processes PDF content with LLaMA 2, generates AI-based summaries. |
| **vm4**     | `3.142.40.244` | MySQL Database                | Stores processed data and metadata, supports querying via APIs. |

---

## **Key Technologies**
- **AWS EC2**: Virtual machines hosting the system.
- **Kubernetes**: Orchestrates containerized workloads across VMs.
- **Docker**: Runs services in isolated, portable containers.
- **Ansible**: Automates provisioning and configuration.
- **Kafka**: Message broker for seamless inter-service communication.
- **Zookeeper**: Ensures Kafka’s reliability and coordination.
- **FastAPI**: Lightweight web framework for API development.
- **MySQL**: Relational database for metadata and logs.
- **LLaMA 2**: AI model for summarizing PDF content.
- **Python**: Powers API and text processing logic.

---

## **Features**
### 1. **PDF Upload and Summarization**
- **Upload**: Users upload PDFs through a FastAPI-based web interface (VM1).
- **Processing**: Text is extracted, chunked, and sent to Kafka (VM2).
- **Summarization**: LLaMA 2 processes the content to generate summaries (VM3).
- **Storage**: Summaries and metadata are stored in MySQL (VM4) for querying.

### 2. **Asynchronous Communication**
- **Kafka Topics**: Separate topics for PDF uploads, processing results, and error handling ensure decoupled communication.
- **Zookeeper Coordination**: Manages Kafka nodes and ensures fault tolerance.

### 3. **AI-Powered Summarization**
- Leverages LLaMA 2 to generate concise summaries for uploaded PDFs.
- AI model is containerized for portability and managed by Kubernetes for scalability.

### 4. **Data Storage**
- **MySQL Database**: Efficiently stores metadata and summaries.
- Schema supports fast retrieval and integration with the query API.

---

## **System Workflow**

1. **PDF Upload (VM1)**:
   - Users upload PDFs via the FastAPI interface.
   - Python libraries (e.g., `pdfplumber`) extract and preprocess text.

2. **Message Broker (VM2)**:
   - Kafka manages communication between components, ensuring reliable delivery of messages.
   - Zookeeper ensures consistency of Kafka’s distributed nodes.

3. **AI Processing (VM3)**:
   - Text is processed by a containerized LLaMA 2 model.
   - Summaries are returned to Kafka for onward delivery to VM4.

4. **Storage and Querying (VM4)**:
   - MySQL stores processed data and metadata.
   - Queries can retrieve summaries and metadata using APIs hosted on VM1.

---

## **Setup Instructions**

### **Step 1: Infrastructure Deployment**
1. Launch four EC2 instances on AWS, ensuring:
   - Operating System: Ubuntu 22.04
   - Security Group: Open necessary ports (e.g., 22 for SSH, 80/8080 for API access, 3306 for MySQL).
   - Key Pair: Use your AWS key pair to SSH into the VMs.

2. Note the public IPs of the VMs and update the `inventory` file.

### **Step 2: Configure Kubernetes and Deploy Services**
1. **Install Dependencies**:
   - Use `playbook_install_apt_packages.yaml` to install required packages.
   - Run `playbook_install_docker.yaml` to set up Docker.

2. **Set Up Kubernetes**:
   - Initialize the Kubernetes master node (VM1) with:
     ```bash
     kubeadm init --pod-network-cidr=192.168.0.0/16
     ```
   - Join the worker nodes (VM2, VM3, VM4) using the token from the master.

3. **Deploy Microservices**:
   - Use Kubernetes manifests (`yaml` files) to deploy the following:
     - FastAPI for PDF uploads (VM1).
     - Kafka and Zookeeper (VM2).
     - LLaMA 2 AI Model (VM3).
     - MySQL Database (VM4).

### **Step 3: Verify the Deployment**
1. Check Kubernetes nodes:
   ```bash
   kubectl get nodes
   ```
2. Verify FastAPI endpoints:
   - Access `http://<VM1_IP>:8080/docs` to test the upload API.
3. Test Kafka messaging and MySQL database connectivity.

---

## **Future Enhancements**
1. **Monitoring**:
   - Integrate Prometheus and Grafana to monitor API performance, resource utilization, and Kafka logs.
2. **Security**:
   - Use TLS for secure communication.
   - Implement Role-Based Access Control (RBAC) for Kubernetes.
3. **Scaling**:
   - Configure horizontal pod autoscaling for AI services to handle increased traffic.

---

## **Contributing**
1. **Fork the Repository**.
2. **Create a Feature Branch**:
   ```bash
   git checkout -b <feature-name>
   ```
3. **Commit Changes**:
   ```bash
   git commit -m "Add <feature>"
   ```
4. **Push Changes**:
   ```bash
   git push origin <feature-name>
   ```
5. **Open a Pull Request** for review.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### **Improvements**
- Clear structure and professional tone.
- Detailed instructions for setup and deployment.
- Added a system workflow for clarity.
- Improved the "Future Enhancements" section with actionable points.
- Used tables and markdown formatting for readability.

Let me know if you’d like further refinements or additional sections!