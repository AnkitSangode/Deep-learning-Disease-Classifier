from diseaseClassifier.config.configuration import ConfigurationManager
from diseaseClassifier.components.data_ingestion import DataIngestion
from diseaseClassifier import logger


STAGE_NAME = "Data Ingestion"
class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion()
            data_ingestion = DataIngestion(config = data_ingestion_config)
            data_ingestion.download_file()
            data_ingestion.exctract_zip_file()
        except Exception as e:
            raise e
        
if __name__ == '__main__':
    try:
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<")
        obj = DataIngestionPipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<< \n\nx==============x")
    except Exception as e:
        logger.exception(e)
