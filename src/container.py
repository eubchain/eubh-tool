from api import Api
from click import echo
from apscheduler.schedulers.background import BlockingScheduler

already_read_log = []


class Container:
    def __init__(self, key):
        self.key = key
        self.api = Api(key)

    def lists(self):
        resp = self.api.get_project_container_lists(self.key)
        for container in resp:
            echo(container)

    def log(self, container_id, is_watch=False, default_loop_time=20):
        if is_watch:
            scheduler = BlockingScheduler()
            scheduler.add_job(self.output_log_single(container_id=container_id), 'interval', seconds=default_loop_time)
            try:
                scheduler.start()
            except (KeyboardInterrupt, SystemExit):
                scheduler.shutdown()
        else:
            self.output_log_single(container_id=container_id)

    def output_log_single(self, container_id):
        resp = self.api.get_project_container_logs_by_container_id(container_id=container_id)
        for container_log_text in resp:
            if container_log_text not in already_read_log:
                echo(container_log_text)
                already_read_log.append(container_log_text)
