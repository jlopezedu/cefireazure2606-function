import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient


app = func.FunctionApp()

@app.blob_trigger(
    arg_name="myblob",
    path="entrada/{name}",
    connection="AzureWebJobsStorage"
)
def copy_blob(myblob: func.InputStream):

    blob_name = myblob.name.split("/")[-1]

    logging.info(
        f"Nuevo archivo detectado: {blob_name}"
    )

    connection_string = (
        "DefaultEndpointsProtocol=https;"
    )

    blob_service_client = (
        BlobServiceClient.from_connection_string(
            connection_string
        )
    )

    source_container = "comprimidos"
    destination_container = "descomprimidos"

    source_blob = (
        blob_service_client
        .get_blob_client(
            source_container,
            blob_name
        )
    )

    destination_blob = (
        blob_service_client
        .get_blob_client(
            destination_container,
            blob_name
        )
    )

    destination_blob.start_copy_from_url(
        source_blob.url
    )

    logging.info(
        f"Archivo copiado: {blob_name}"
    )
