from src.diseaseClassifier.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from src.diseaseClassifier import logger


STAGE_NAME = "Data Ingestion"


if __name__ == '__main__':
    try:
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<")
        obj = DataIngestionPipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<< \n\nx==============x")
    except Exception as e:
        logger.exception(e)
