import json
import os

from google.cloud.vision_helpers import VisionHelpers
from google.cloud.vision_helpers.decorators import add_single_feature_methods
from google.cloud.vision_v1 import types
from google.cloud.vision_v1.gapic import enums
from google.cloud.vision_v1.gapic import image_annotator_client as iac
from google.oauth2 import service_account


@add_single_feature_methods
class ImageAnnotatorClient(VisionHelpers, iac.ImageAnnotatorClient):
    __doc__ = iac.ImageAnnotatorClient.__doc__
    enums = enums

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)


def detect_labels_uri(uri):
    credentials_data = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    service_account_info = json.loads(credentials_data)
    credentials = service_account.Credentials.from_service_account_info(service_account_info)

    client = ImageAnnotatorClient(credentials=credentials)
    image = types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    if response.error.message:
        raise Exception(
            f'{response.error.message}For more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors')

    return (
        {
            'score': label.score,
            'description': label.description,
        }
        for label in labels
    )
