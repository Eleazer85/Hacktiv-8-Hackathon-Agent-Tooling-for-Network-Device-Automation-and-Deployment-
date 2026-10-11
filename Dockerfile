FROM langflowai/langflow:latest

# Download composio & other components
RUN pip install --no-cache-dir \
   composio \
   composio_langchain \
   lfx-bundles \
   requests \
   paramiko \
   librouteros \