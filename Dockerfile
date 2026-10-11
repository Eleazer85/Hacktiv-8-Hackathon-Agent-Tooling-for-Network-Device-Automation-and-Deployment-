FROM langflowai/langflow:latest

# Composio support: the SDK, the LangChain provider it needs,
# and the lfx-bundles package that actually contains the
# Langflow-facing components (moved out of lfx/langflow core).
RUN pip install --no-cache-dir \
   composio \
   composio_langchain \
   lfx-bundles \
   requests \
   paramiko \
   librouteros \