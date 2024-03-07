from locust import HttpUser, task, between
from models.machines import Template
import random
import logging


class HelloWorldUser(HttpUser):

    @task
    def get_machines(self):
        endppoint = "/api/v1/machines/"
        resp = self.client.get(endppoint)
        logging.info(
            "Getting data from endpoint %s - with response: %s (total number of machines %d)",
            endppoint,
            resp,
            len(resp.json()),
        )
        return resp.json()

    def get_machine(self, idx: int) -> dict:
        endpoint = f"/api/v1/machines/{idx}"
        resp = self.client.get(endpoint)
        logging.info(
            "Getting data from endpoint %s - with response: %s (total number of machines %d)",
            endpoint,
            resp,
            len(resp.json()),
        )
        return resp.json()

    @task
    def set_machine(self):
        endpoint = "/api/v1/machines/"
        template_value = random.choice(list(Template))

        with self.client.post(
            endpoint,
            json={"custom_name": "foo", "template": template_value},
            catch_response=True,
        ) as resp:
            machine_id = resp.json().get("machine_id")
            logging.info(
                "Created another machine of type %s (id %s) with response: %s (%s)",
                template_value,
                machine_id,
                resp,
                resp.text,
            )
            if machine_id is None:
                err_msg = "Device creation failed"
                logging.error(err_msg)
                resp.failure(err_msg)
                return

            machine = self.get_machine(resp.json().get(machine_id))
            if machine.get("template") != template_value:
                err_msg = "Obtained template value differs from the created one!"
                logging.error(err_msg)
                resp.failure(err_msg)

    @task
    def delete_machine(self):
        machine_id = random.choice(self.get_machines()).get("machine_id", 0)

        endpoint = f"/api/v1/machines/{machine_id}"
        resp = self.client.delete(endpoint)
        logging.info(
            "Deleting a machine: machine ID %s with response: %s",
            machine_id,
            resp,
        )
