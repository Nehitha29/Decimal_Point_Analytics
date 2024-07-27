


### Introduction
This project is designed with a microservices architecture using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python. Each microservice operates independently on different backend ports, providing distinct functionalities like user login, points retrieval, review handling, and link management. The microservices communicate with each other through well-defined APIs, ensuring a modular, scalable, and maintainable system.

Architecture Overview
The system comprises several microservices, each dedicated to a specific functionality:

1.Authentication Service- port 8008


2.Points Service-port 8050


3.Review Service -port 8000,8001,9001,


4.Link Management Service- port 9009


5.commnet services -  port 8003

### HOW TO RUN ??
uvicorn main:app --reload --port portnumber


uvicorn folder:main:app --reload   --port portnumber 

https://github.com/user-attachments/assets/7fd03034-8e9e-43f2-a7f8-d70dda86f707
