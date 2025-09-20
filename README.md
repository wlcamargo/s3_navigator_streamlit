# S3 Navigator - Streamlit
This project provides a file browser for S3-compatible storage (tested with MinIO) built with Python and Streamlit.
It allows users to navigate through buckets and folders, preview common file formats (CSV, Parquet, Excel, TXT, images), open files directly in the interface, and manage uploads and downloads in a simple and user-friendly way.

## APP Layout
![Architecture Diagram](assets/layout.png)

## Prerequisites
- Git
- Docker
- Docker Compose
- Python 3.7+ (recommended)

## Libs
```
streamlit==1.46.0
boto3==1.40.6
python-dotenv==1.1.1
```

## Infra
### Docker
Docker is a containerization platform that packages applications and their dependencies into isolated containers to run anywhere.

### MinIO / S3
MinIO is a high-performance, S3-compatible object storage server. It supports the Amazon S3 API, enabling use of existing S3 tools and SDKs.

## How to Install Docker?
You can follow this tutorial: 

https://www.youtube.com/watch?v=pRFzDVn40rw&list=PLbPvnlmz6e_L_3Zw_fGtMcMY0eAOZnN-H

## How to Use the Project?
Clone the repository:
```
git clone https://github.com/wlcamargo/s3_navigator_streamlit.git
```
```
cd s3_navigator_streamlit
```

## How to Start the MinIO Container?

```
cd src/minio
docker compose up -d
```

### How to Access Minio?
Open your browser and go to:

http://localhost:9000

Minio Credentials  
| Username  | Password    |  
| --------- | ----------- |  
| chapolin  | mudar@123   |

### How to run front end?

#### Create a Virtual Environment (optional, but recommended)

##### On Linux/macOS:

```bash 
python3 -m venv venv
```
##### On Windows:

```bash Windows
python -m venv venv
```

#### Activate the Virtual Environment

##### On Linux/macOS:

```bash
source venv/bin/activate
```

##### On Windows:

```bash
venv\Scripts\activate
```

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Execute the command to start application
```
cd src/
streamlit run app.py
```

Open your browser and go to:

http://localhost:8501


## 📚 References
- [Streamlit docs](https://docs.streamlit.io)  
- [MinIO docs](https://min.io/docs/)  
- [AWS S3 docs](https://docs.aws.amazon.com/s3/index.html)

## 🧑🏼‍🚀 Developer
| Developer      | LinkedIn   | Email               | Portfolio   |  
| -------------- | ---------- | ------------------- | ----------- |  
| Wallace Camargo | [LinkedIn](https://www.linkedin.com/in/wallace-camargo-35b615171/) | wallacecpdg@gmail.com | [Portfólio](https://wlcamargo.github.io/)  |  
