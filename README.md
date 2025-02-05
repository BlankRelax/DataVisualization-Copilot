
https://github.com/user-attachments/assets/05663a3d-b0d4-4f66-b0bc-ac8ac969f88e
# DataVisualization Copilot

## What it does ?

From Natural langauge (NL) to SQL to a data visualization using the power of LLMs and Apache Superset (visualization engine)
This API client connects to your superset instance and allows you to enter a NL request, the output of which is a graph.

## Tech stack
- Python Backend
- JS and TS Frontend
- Docker for containerization

## Live Demo




https://github.com/user-attachments/assets/10c9fb1c-1730-424c-90f2-7c6ac41f3574

## How did I achieve this?

I built a client that connects to the Apache Superset instance. Superset is an open source data visualization engine that provides REST APIs for their application, allowing you to connect databases, create tables from SQL queries and create charts from those tables. 
So essentially, this client utilizes this feature to build its own application on top of an existing application, the modified frontend is actually a part of the open source code base. The app on top of an app acts like an expansion feature its is optional.

Below shows an architecture diagrams of how the Superset add-on interacts with the Superset Application 
![CareCognetics SysArchitecture drawio](https://github.com/user-attachments/assets/0ce30407-c489-4265-abc7-93d14afbd94d)

### API Flow
![supersetAPI_flow drawio](https://github.com/user-attachments/assets/5ed4ecd1-e01e-4464-b91b-dbf9ad28b6e2)

### Detailed Flow
![Application_architecture drawio](https://github.com/user-attachments/assets/fa696877-e787-4243-a514-ffd5543b1bd1)
