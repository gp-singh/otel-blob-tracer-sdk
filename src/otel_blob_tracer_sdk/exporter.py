from azure.storage.blob import BlobServiceClient
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
import json

class AzureBlobExporter(SpanExporter):
    def __init__(self, connection_string: str, container_name: str, prefix:str="traces/") -> None:
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)
        if not self.container_client.exists():
            self.container_client.create_container(container_name)
        self.prefix = prefix

    def export(self, spans) -> SpanExportResult:
        try:
            payload = [self._span_to_dict(span) for span in spans]
            trace_id = getattr(spans[0].context, "trace_id", "no-trace") if spans else "no-trace"
            blob_name = f"{self.prefix}trace-{trace_id}.json"
            blob = self.container_client.get_blob_client(blob_name)
            blob.upload_blob(json.dumps(payload, indent=2), overwrite=True)
            return SpanExportResult.SUCCESS
        except Exception:
            return SpanExportResult.FAILURE

    def _span_to_dict(self, span):
        return {
            "name": span.name,
            "attributes": dict(getattr(span, "attributes", {})),
            "start_time": getattr(span, "start_time", None),
            "end_time": getattr(span, "end_time", None),
        }


    def shutdown(self) -> None:
        pass
