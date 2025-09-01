from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.attributes import SpanAttributes
from .exporter import AzureBlobExporter

def init_tracer(conn_str: str, container: str):
    provider = TracerProvider()
    exporter = AzureBlobExporter(conn_str, container)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    return trace.get_tracer(__name__)

def trace_genai_call(tracer, model: str, input_tokens: int, output_tokens: int):
    with tracer.start_as_current_span("genai.call") as span:
        span.set_attribute(SpanAttributes.GEN_AI_MODEL, model)
        span.set_attribute(SpanAttributes.GEN_AI_INPUT_TOKENS, input_tokens)
        span.set_attribute(SpanAttributes.GEN_AI_OUTPUT_TOKENS, output_tokens)