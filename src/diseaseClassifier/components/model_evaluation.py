import tensorflow as tf
from pathlib import Path
import mlflow
from diseaseClassifier.utils.common import save_json
from urllib.parse import urlparse
from diseaseClassifier.entity import EvaluationConfig

class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config
    
    def _valid_generator(self):

        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split = 0.30
        )

        dataflow_kwargs = dict(
            target_size = self.config.params_image_size[:-1],
            batch_size = self.config.params_batch_size,
            interpolation = "bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory = self.config.training_data,
            subset= "validation",
            shuffle = False,
            **dataflow_kwargs
        )

    @staticmethod
    def load_model(path:Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)
    
    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self._valid_generator()
        self.score = model.evaluate(self.valid_generator)
        self.save_score()

    def save_score(self):
        scores = {"loss":self.score[0],"accuracy":self.score[1]}
        save_json(path=Path("score.json"),data= scores)

    def log_into_mlflow(self):
        mlflow.set_registry_uri(self.config.mlflow_uri)
        

        with mlflow.start_run():
            mlflow.log_params(self.config.all_params)
            mlflow.log_metrics(
                {"loss":self.score[0],"accuracy": self.score[1]}
            )

            # 1. Save locally
            self.model.save(self.config.path_of_model)  # creates a directory

            # 2. Log directory as artifact
            mlflow.log_artifacts(self.config.path_of_model, artifact_path="model")
