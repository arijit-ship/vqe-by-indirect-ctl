import json
import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Job:
    id: str
    creation_time: datetime
    execution_second: int
    nqubit: int
    depth: int
    gate_type: str
    gate_set: str
    bn_type: str
    bn_range: int
    bn: str
    cn: str
    r: str
    t_type: str
    max_time: str
    min_time: str
    t: str
    cost: str
    parameter: str
    iteration: str
    cost_history: str
    parameter_history: str
    iteration_history: str
    noise_singlequbit_enabled: str
    noise_singlequbit_value: str
    noise_twoqubit_enabled: str
    noise_twoqubit_value: str
    config: str


class JobFactory:
    def __init__(self, config):
        self.config = config
        pass

    def _to_string(self, two_dim_array):
        s = ""
        for i in range(len(two_dim_array)):
            s += ",".join([str(j) for j in two_dim_array[i]])
            if i == len(two_dim_array):
                break

            s += "\n"

        return s

    def create(
        self,
        current_time: datetime,
        start_time: float,
        end_time: float,
        cost_history: list[float],
        param_history: list[float],
        iter_history: list[int],
    ) -> Job:
        if self.config["gate"]["type"] == "direct":
            job = self._create_job_for_direct(
                current_time,
                start_time,
                end_time,
                cost_history,
                param_history,
                iter_history,
            )
        else:
            job = self._create_job_for_indirect(
                current_time,
                start_time,
                end_time,
                cost_history,
                param_history,
                iter_history,
            )
        return job

    def _create_job_for_direct(
        self,
        current_time: datetime,
        start_time: float,
        end_time: float,
        cost_history: list[float],
        param_history: list[float],
        iter_history: list[int],
    ) -> Job:
        return Job(
            str(uuid.uuid4()),
            current_time,
            end_time - start_time,
            self.config["nqubit"],
            self.config["depth"],
            self.config["gate"]["type"],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            str(cost_history[-1]),
            str(param_history[-1]),
            str(iter_history[-1]),
            str(cost_history),
            self._to_string(param_history),
            str(iter_history),
            self.config["gate"]["noise"]["singlequbit"]["enabled"],
            self.config["gate"]["noise"]["singlequbit"]["value"]
            if "value" in self.config["gate"]["noise"]["singlequbit"]
            else None,
            self.config["gate"]["noise"]["twoqubit"]["enabled"],
            self.config["gate"]["noise"]["twoqubit"]["value"]
            if "value" in self.config["gate"]["noise"]["twoqubit"]
            else None,
            json.dumps(self.config),
        )

    def _create_job_for_indirect(
        self,
        current_time: datetime,
        start_time: float,
        end_time: float,
        cost_history: list[float],
        param_history: list[float],
        iter_history: list[int],
    ) -> Job:
        return Job(
            str(uuid.uuid4()),
            current_time,
            end_time - start_time,
            self.config["nqubit"],
            self.config["depth"],
            self.config["gate"]["type"],
            str(self.config["gate"]["parametric_rotation_gate_set"]),
            str(self.config["gate"]["bn"]["type"]),
            self.config["gate"]["bn"]["range"]
            if "range" in self.config["gate"]["bn"]
            else None,
            str(self.config["gate"]["bn"]["value"]),
            str(self.config["gate"]["cn"]["value"]),
            str(self.config["gate"]["r"]["value"]),
            self.config["gate"]["time"]["type"],
            self.config["gate"]["time"]["max_val"]
            if "max_val" in self.config["gate"]["time"]
            else None,
            self.config["gate"]["time"]["min_val"]
            if "min_val" in self.config["gate"]["time"]
            else None,
            str(self.config["gate"]["time"]["value"])
            if "value" in self.config["gate"]["time"]
            else None,
            str(cost_history[-1]),
            str(param_history[-1]),
            str(iter_history[-1]),
            str(cost_history),
            self._to_string(param_history),
            str(iter_history),
            self.config["gate"]["noise"]["singlequbit"]["enabled"],
            self.config["gate"]["noise"]["singlequbit"]["value"]
            if "value" in self.config["gate"]["noise"]["singlequbit"]
            else None,
            self.config["gate"]["noise"]["twoqubit"]["enabled"],
            self.config["gate"]["noise"]["twoqubit"]["value"]
            if "value" in self.config["gate"]["noise"]["twoqubit"]
            else None,
            json.dumps(self.config),
        )
