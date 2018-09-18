from django.db.models import Manager
from .model_status import customer_state


class CustomerManager(Manager):

    def create_init_customer(self, contact_name, contact_mobile, company_name):
        init_customer = self.create(contact_name=contact_name,
                                    contact_mobile=contact_mobile,
                                    company_name=company_name,
                                    status=customer_state['INIT'])
        return init_customer

    def update_connected_status(self, pk):
        connected_customer = self.filter(pk=pk).first()
        if connected_customer:
            connected_customer.status = customer_state['CONNECTED']
            connected_customer.save()
            return connected_customer
