from typing_cc.typing import supported_viz_types, supported_viz_types_inv 

class UnsupportedViztypeError(Exception):
    """Exception raised for unsupported viz_types.

    Attributes:
        viz_type -- internal name for chart type
        message -- the vizualization chosen is not currently supported, pick another one amongst the supported ones
    """
     
    def __init__(self, viz_type:str):
        self.viz_type = viz_type
        self.message= f"{self.viz_type} is not supported. Choose from the following: {supported_viz_types}"
        super().__init__(self.message)

class DatasetNotCreatedError(Exception):
    """Exception raised when a dataset cannot be created through SupersetAPIClient

    Attributes:
        viz_type -- internal name for chart type
        message -- failed to create dataset- check for duplicates
    """
     
    def __init__(self, dataset_name:str,r_error:str):
        self.dataset_name = dataset_name
        self.r_error=r_error
        self.message= f"{self.dataset_name} could not be created. Request error code : {self.r_error} - Could not process entity"
        super().__init__(self.message)

class DatabaseNotAccessedError(Exception):
    """Exception raised when GET database API endpoint fails

    Attributes:
        viz_type -- internal name for chart type
        message -- database API endpoint cannot be accessed
    """
     
    def __init__(self):
        self.message= f"Databases could not be accessed"
        super().__init__(self.message)

class DatabaseSchemaNotAccessedError(Exception):
    """Exception raised when a specific database schema cannot be accessed by superset API database/{pk}/schemas/ endpoint

    Attributes:
        database_name -- database name trying to be accessed
        message -- database may not exist, database_name may be entered incorrectly
    """
     
    def __init__(self, database_name:str):
        self.database_name=database_name
        self.message= f"schemas for {self.database_name} cannot be accessed"
        super().__init__(self.message)

"""responses = {
        "400": {"description": "Bad request", "content": error_payload_content},
        "401": {"description": "Unauthorized", "content": error_payload_content},
        "403": {"description": "Forbidden", "content": error_payload_content},
        "404": {"description": "Not found", "content": error_payload_content},
        "410": {"description": "Gone", "content": error_payload_content},
        "422": {
            "description": "Could not process entity",
            "content": error_payload_content,
        },
        "500": {"description": "Fatal error", "content": error_payload_content},"""