import streamlit as st
import boto3
from botocore.client import Config
import os
import pandas as pd
from io import BytesIO

#----- S3 (MinIO) client configuration -----#
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",  # adjust to your MinIO endpoint
    aws_access_key_id="chapolin",
    aws_secret_access_key="mudar@123",
    config=Config(signature_version="s3v4"),
    region_name="us-east-1"
)

st.set_page_config(page_title="S3 Browser - MinIO", layout="wide")

st.title("🌐 S3 Navigator")

#----- Select bucket -----#
buckets = [b["Name"] for b in s3.list_buckets()["Buckets"]]
bucket = st.sidebar.selectbox("Select a bucket", buckets)

#----- Current folder state -----#
if "prefix" not in st.session_state:
    st.session_state.prefix = ""

#----- Back button -----#
if st.session_state.prefix:
    if st.sidebar.button("⬅️ Back"):
        st.session_state.prefix = "/".join(st.session_state.prefix.strip("/").split("/")[:-1])
        if st.session_state.prefix:
            st.session_state.prefix += "/"

#----- List objects and "folders" -----#
response = s3.list_objects_v2(Bucket=bucket, Prefix=st.session_state.prefix, Delimiter="/")

st.subheader(f"📂 {bucket}/{st.session_state.prefix}")

#----- Show folders -----#
if "CommonPrefixes" in response:
    for cp in response["CommonPrefixes"]:
        folder = cp["Prefix"].split("/")[-2]  # folder name
        if st.button(f"📁 {folder}"):
            st.session_state.prefix = cp["Prefix"]

#----- Show files -----#
if "Contents" in response:
    for obj in response["Contents"]:
        key = obj["Key"]
        if key.endswith("/"):  # ignore folders
            continue
        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        col1.write(f"📄 {os.path.basename(key)}")
        
        #----- Preview -----#
        if col2.button("👁", key=f"view_{key}", help="Preview file content"):
            file_obj = s3.get_object(Bucket=bucket, Key=key)
            data = file_obj["Body"].read()
            try:
                if key.endswith(".csv"):
                    df = pd.read_csv(BytesIO(data))
                    st.dataframe(df)
                elif key.endswith(".parquet"):
                    df = pd.read_parquet(BytesIO(data))
                    st.dataframe(df)
                elif key.endswith((".xls", ".xlsx")):
                    df = pd.read_excel(BytesIO(data))
                    st.dataframe(df)
                elif key.endswith(".txt") or key.endswith(".log"):
                    st.text(data.decode("utf-8")[:2000])  # limited preview
                elif key.endswith((".png", ".jpg", ".jpeg")):
                    st.image(data)
                elif key.endswith(".pdf"):
                    st.info("PDF preview not implemented. Download to view.")
                else:
                    st.info("File preview not supported.")
            except Exception as e:
                st.error(f"Error reading file: {e}")

        #----- Download -----#
        if col3.download_button("⬇️", data=s3.get_object(Bucket=bucket, Key=key)["Body"].read(),
                                file_name=os.path.basename(key)):
            st.success(f"Downloaded {key}")

        #----- Open -----#
        if col4.button("🔓", key=f"open_{key}", help="Open file"):
            st.write(f"### Opened file: {key}")
            file_obj = s3.get_object(Bucket=bucket, Key=key)
            data = file_obj["Body"].read()
            try:
                if key.endswith(".csv"):
                    df = pd.read_csv(BytesIO(data))
                    st.dataframe(df.head(50))  # show first 50 rows
                elif key.endswith(".parquet"):
                    df = pd.read_parquet(BytesIO(data))
                    st.dataframe(df.head(50))
                elif key.endswith((".xls", ".xlsx")):
                    df = pd.read_excel(BytesIO(data))
                    st.dataframe(df.head(50))
                else:
                    # fallback: try as text
                    st.text(data.decode("utf-8")[:2000])
            except Exception as e:
                st.error(f"Error opening file: {e}")


#----- Upload section -----# 
st.sidebar.subheader("📤 Upload file")
upload_file = st.sidebar.file_uploader("Choose a file to upload")

if upload_file:
    st.sidebar.write(f"Selected file: **{upload_file.name}**")
    if st.sidebar.button("✅ Confirm upload"):
        s3.upload_fileobj(upload_file, bucket, st.session_state.prefix + upload_file.name)
        st.sidebar.success(f"Uploaded {upload_file.name}")
