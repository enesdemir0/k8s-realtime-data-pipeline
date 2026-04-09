# 📈 Real-Time Crypto Data Pipeline on Kubernetes

This project is a full-stack, event-driven microservices pipeline designed to fetch, process, and visualize cryptocurrency data in real-time. It is built to demonstrate professional DevOps practices, microservices communication, and cloud-native orchestration using **Kubernetes (KIND)** and **GitHub Actions**.

## 🏗 System Architecture

```mermaid
graph TD
    A[External Crypto API] -->|HTTPS| B(Service A: Collector)
    B -->|TCP 6379| C{Service B: Redis Broker}
    C -->|Pull| D(Service C: Processor)
    D -->|Logic: Calculate Trend| D
    D -->|TCP 5432| E[(Service D: PostgreSQL)]
    E -->|Persistent Storage| F[PVC: 1GB Disk]
    E -->|Query| G(Service E: Dashboard)
    G -->|Streamlit App| H[User Browser]