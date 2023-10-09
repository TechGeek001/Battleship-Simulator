class World:

    def __init__(self):
        # Generate objects that are in the way - make this better in the future
        self.obstacles = [
            [(260, 320), (365,350), (270,440), (260, 320)]
        ]
        self.logging_variables = ["total_time", "timedelta"]
        self.total_time = 0
        self.timedelta = 0
        self.models = {}
    
    def update(self, timedelta):
        self.total_time += timedelta
        self.timedelta = timedelta
        for model in self.models.values():
            model.update(timedelta)
    
    def logging_package(self):
        logging_package = {k: getattr(self, k) for k in self.logging_variables}
        for model_name, model in self.models.items():
            model_log_package = model.logging_package()
            for k, v in model_log_package.items():
                logging_package[f"{model_name}.{k}"] = v
        return logging_package

    def attach_model(self, model, name):
        self.models[name] = model
        model.world = self