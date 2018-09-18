from apps.util.wrapper import verify_eth_address
from apps.user.models import UserProfile


def validate_withdraw(user_id,
                      bbn_count,
                      wallet_address):
    res = dict()
    res['count_error'] = list()
    res['address_error'] = list()
    verify_address_ret = verify_eth_address(wallet_address)
    user = UserProfile.objects.get(pk=user_id)
    bbn_balance = user.bbn_count

    if not bbn_balance or bbn_balance < 100:
        res['count_error'].append("余额不足,无法提现")
    if not bbn_count:
        res['count_error'].append("bbn数量不足")
    if not wallet_address:
        res['address_error'].append("钱包地址不能为空")
    if bbn_count < 100:
        res['count_error'].append("提现数量必须大于100个")
    if bbn_count > bbn_balance:
        res['count_error'].append("提现数量不能大于账户余额")
    if bbn_count % 100 != 0:
        res['count_error'].append("提现数量必须为100的整数倍")
    if not verify_address_ret:
        res['address_error'].append("钱包地址不合法")
    if res['count_error'] or res['address_error']:
        return res

