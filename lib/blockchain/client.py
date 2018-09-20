import time
import logging
import hashlib
import requests
from apps.mtc.models import MtcUser

django_logger = logging.getLogger('django')


class MTC:
    def __init__(self):
        self._request = requests
        self._logger = django_logger
        # MTC server
        self.base_url = 'MTC server'
        # MTC Token
        self.token = 'MTC Token'
        # MTC SecretKey
        self.secret_key = 'MTC SecretKey'

    def _generate_customer_id(self, user_id: int):
        return self._md5(str(user_id))

    @staticmethod
    def _md5(raw_str):
        return hashlib.new("md5", raw_str.encode('utf8')).hexdigest()

    @staticmethod
    def _format_int_time(num_time):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(num_time))

    def get_now(self):
        return self._format_int_time(int(time.time()))

    def _build_up_param(self,
                        customer_id: str,
                        agreement_number: str,
                        channel: str,
                        device_info: str,
                        date: str,
                        launch_action: str,
                        param_info: str):
        """
        :return: dict object
        """
        request_param = dict()
        request_param["customerId"] = customer_id
        request_param['secretKey'] = self.secret_key
        request_param["agreementNumber"] = agreement_number
        request_param['channel'] = channel
        request_param['deviceInfo'] = device_info
        request_param['date'] = date
        request_param['launchAction'] = launch_action
        request_param['paramInfo'] = param_info
        return request_param

    def _validate_txid(self, txid):
        if not txid:
            self._logger.info('Null txid')
            return False
        return True

    def _build_up_write_url(self, url: str):
        return '{0}{1}?token={2}'.format(self.base_url, url, self.token)

    def _build_up_read_url(self, url: str, txid: str):
        return '{0}{1}?txHash={2}'.format(self.base_url, url, txid)

    @staticmethod
    def _load_param_info(customer_id):
        return "id:{}".format(customer_id)

    def write_to_eth(self,
                     device_info: str,
                     frog_user_id: int,
                     agreement_number: str,
                     channel: str,
                     launch_action: str):
        """
        :return:resp_data or None
        """
        frog_user = MtcUser.objects.filter(pk=frog_user_id).first()
        customer_id = self._generate_customer_id(frog_user_id)
        param_info = self._load_param_info(customer_id)
        date = self.get_now()
        self._logger.info('Start request write_to_eth, customerId:{}'.format(customer_id))
        request_param = self._build_up_param(customer_id, agreement_number, channel, device_info,
                                             date, launch_action, param_info)
        frog_user.save_write_info(eth_parameters=request_param)
        try:
            resp = self._request.post(self._build_up_write_url('/v2/authorization'), json=request_param, timeout=120.0)
            resp_data = resp.json()
            self._logger.info('Received customerId:{0} data: {1}'.format(customer_id, resp_data))
            if resp_data and 'data' in resp_data and 'code' in resp_data:
                if resp_data['code'] == '200':
                    frog_user.eth_txid = resp_data['data']
                    frog_user.save()
                else:
                    frog_user.eth_status = 'Fail'
                    frog_user.save()
                    self._logger.info('Fail request write_to_eth')
            return resp_data
        except Exception as e:
            frog_user.eth_status = 'Exception'
            frog_user.save()
            self._logger.info('Exception request write_to_eth error:{0}, customerId:{1}'.format(e, customer_id))

    def read_from_eth(self):
        """
        :return:resp_data or None
        """
        frog_users = MtcUser.objects.fetch_has_txid_instance()
        for frog_user in frog_users:
            txid = frog_user.eth_txid
            self._logger.info('Start request read_from_eth,  txId:{}'.format(txid))
            if self._validate_txid(txid):
                try:
                    resp = requests.get(self._build_up_read_url('/v2/authorization/status', txid), params={}, timeout=120.0)
                    resp_data = resp.json()
                    self._logger.info('Received txId:{0} data {1} '.format(txid, resp_data))
                    if resp_data and 'data' in resp_data and 'code' in resp_data:
                        if resp_data['code'] == '200':
                            frog_user.save_read_info(eth_response=resp_data, eth_status=resp_data['data']['txReceiptStatus'])
                    return resp_data
                except Exception as e:
                    self._logger.info('Error request read_from_eth error: {0}, txId:{1}'.format(e, txid))

