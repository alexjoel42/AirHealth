from pydantic import BaseModel

class SensorConfig(BaseModel):
    port: str
    baudrate: int
    timeout: int

config = load_config()
validated = SensorConfig(**config["sensor"])