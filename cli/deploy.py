class Deploy(object):
    """
    Handles the deployment process
    """
    def __init__(self, project_id, instance_name, instance_zone, instance_type, instance_start, instance_image):
        self.project_id = project_id
        self.instance_name = instance_name
        self.instance_zone = instance_zone
        self.instance_type = instance_type
        self.instance_meta = "start-script=" + instance_start
        self.instance_image = instance_image
        self.deploy_cmd = []

    def __init__(self):
        pass

    def build_cmd(self):
        """
        Builds the gcloud-cli command for deploying a machine.
        """
        # start command
        self.deploy_cmd.append("gcloud compute")
        # append command options
        self.deploy_cmd.append("--project")
        self.deploy_cmd.append(self.config.get("gcloud", "project_id"))
        self.deploy_cmd.append("instances create docker-test-1")
        self.deploy_cmd.append("--zone")
        self.deploy_cmd.append(self.config.get("gcloud", "zone"))
        self.deploy_cmd.append("--machine-type")
        self.deploy_cmd.append(self.config.get("gcloud", "machine"))
        self.deploy_cmd.append("--network default")
        self.deploy_cmd.append("--metadata")
        self.deploy_cmd.append(self.config.get("repo", "start_script"))
        self.deploy_cmd.append("--image")
        self.deploy_cmd.append(self.config.get("glcoud", "image"))
        return self.deploy_cmd

    def start_deploy(self):
        print "huhu"
        print self.deploy_cmd




