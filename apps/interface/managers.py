from django.db.models import Manager


class InterfaceManager(Manager):

    def find_by_id(self, pk):
        return self.filter(pk=pk).first()


class InterfaceParamManager(Manager):

    def find_request_param_by_id(self, pk):
        return self.filter(interface_id=pk, is_res=True)

    def find_response_param_by_id(self, pk):
        return self.filter(interface_id=pk, is_res=False)


class InterfaceExampleManager(Manager):

    def find_request_example_by_id(self, pk):
        return self.filter(interface_id=pk, is_res=True)

    def find_response_example_by_id(self, pk):
        return self.filter(interface_id=pk, is_res=False)
