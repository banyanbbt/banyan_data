# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.db import models

from apps.product.models import AccountProduct

from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _


def get_week_range(year, month, week):
    month_first_day = datetime.date(year=year, month=month, day=1)

    # month first day is friday
    if month_first_day.weekday() == 4:
        week_first_day = month_first_day + datetime.timedelta(weeks=week)
    else:
        week_first_day = month_first_day + datetime.timedelta(weeks=week - 1)
    week_day = week_first_day.weekday()

    if week_day != 4:
        prev_friday = week_first_day - datetime.timedelta(days=(week_day - 4) % 7)
        cur_thursday = week_first_day + datetime.timedelta(days=(3 - week_day) % 7)
    else:
        prev_friday = week_first_day - datetime.timedelta(days=week_day) + datetime.timedelta(days=4, weeks=-1)
        cur_thursday = week_first_day - datetime.timedelta(days=1)

    return prev_friday, cur_thursday


def get_month_range(year, month):
    first_day = datetime.date(year, month, 1)
    last_day = (first_day.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

    return first_day, last_day


class BaseBillModel(models.Model):
    account = models.CharField(_('账号'), max_length=16)
    product = models.CharField(_('产品编码'), max_length=16)
    request_count = models.IntegerField(_('请求次数'))
    bill_count = models.IntegerField(_('计费次数'))
    total_amount = models.DecimalField(_('计费金额'), max_digits=19, decimal_places=2)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def billing_dict(cls, account, year, month, week=None):
        tmp = dict()
        queryset = cls.objects.filter(account=account)

        if year and month and week:
            prev_friday, cur_thursday = get_week_range(int(year), int(month), int(week))
            qs = queryset.filter(begin_day_at__gte=prev_friday, end_day_at__lte=cur_thursday)
        else:
            qs = queryset.filter(month_at__year=year, month_at__month=month)

        for inst in qs:
            tmp[inst.product] = model_to_dict(inst, fields=['request_count', 'bill_count', 'total_amount'])

        return list(qs.values_list('product', flat=True)), tmp

    @classmethod
    def billing_lst(cls, account, year, month, week=None):
        lst = list()
        queryset = cls.objects.filter(account=account)

        if year and month and week:
            prev_friday, cur_thursday = get_week_range(int(year), int(month), int(week))
            qs = queryset.filter(begin_day_at__gte=prev_friday, end_day_at__lte=cur_thursday).order_by('pk')
        else:
            qs = queryset.filter(month_at__year=year, month_at__month=month).order_by('pk')

        for inst in qs:
            lst.append(model_to_dict(inst, fields=['product', 'request_count', 'bill_count', 'total_amount']))

        return list(qs.values_list('product', flat=True)), lst

    @classmethod
    def summary(cls, account, year, month, week=None):
        queryset = cls.objects.filter(account=account)

        if year and month and week:
            start_day, end_day = get_week_range(int(year), int(month), int(week))
            qs = queryset.filter(begin_day_at__gte=start_day, end_day_at__lte=end_day)
        else:
            qs = queryset.filter(month_at__year=year, month_at__month=month)
            start_day, end_day = get_month_range(int(year), int(month))

        query_dict = qs.aggregate(sum_request=models.Sum('request_count'), sum_bill=models.Sum('bill_count'),
                                  sum_total=models.Sum('total_amount'))
        query_dict['account'] = account
        query_dict['count'] = len(set(qs.values_list('product', flat=True)))
        query_dict['start_day'] = start_day
        query_dict['end_day'] = end_day

        return query_dict

    @classmethod
    def max_updated_at(cls, account):
        record = cls.objects.filter(account=account).order_by('-updated_at').first()
        if record:
            return round(record.updated_at.timestamp())
        else:
            now = datetime.datetime.now()
            year = now.year
            last_month = now.month
            if last_month > 1:
                last_month = last_month - 1
            else:
                last_month = 12 - 1
                year = year - 1
            dt = datetime.datetime(year, last_month, 1, 0, 0)
            return round(dt.timestamp())

    @classmethod
    def construct_bill_dict(cls, year, month, week, account):
        if week and month and year:
            lst, bill_dict = BillWeekly.billing_lst(account, int(year), int(month), int(week))
            summary = BillWeekly.summary(account, int(year), int(month), int(week))
        elif year and month:
            lst, bill_dict = BillMonthly.billing_lst(account, year, month)
            summary = BillMonthly.summary(account, int(year), int(month))
        else:
            now = timezone.now()
            lst, bill_dict = BillMonthly.billing_lst(account, now.year, now.month)
            summary = BillMonthly.summary(account, now.year, now.month)

        product_detail = AccountProduct.bill_dict(lst)

        for x in bill_dict:
            if x['product'] in product_detail:
                x.update(product_detail.get(x['product']))

        return summary, bill_dict


class BillDaily(BaseBillModel):
    day_at = models.DateField(_('创建时间'))

    class Meta:
        managed = True
        db_table = 'bill_daily'

    def __str__(self):
        return '%s, %s: %s' % (self.account, self.product, self.total_amount)

    @classmethod
    def build_user_daily_bill(cls, account, params):
        record = cls.objects.filter(account=account, product=params['product'],
            day_at=params['day']).first()
        if record:
            record.request_count = params['requestCount']
            record.bill_count = params['billCount']
            record.total_amount = params['amount']
            record.updated_at = datetime.datetime.fromtimestamp(params['updateAt'])
            record.save()
        else:
            cls.create(account=account, product=params['product'], day_at=params['day'],
                request_count=params['requestCount'], bill_count=params['billCount'],
                total_amount=params['amount'],
                updated_at=datetime.datetime.fromtimestamp(params['updateAt']))



class BillWeekly(BaseBillModel):
    week_in_year = models.IntegerField(_('自然周序数'))
    begin_day_at = models.DateField(_('周开始日期'))
    end_day_at = models.DateField(_('周结束日期'))

    class Meta:
        managed = True
        db_table = 'bill_weekly'

    def __str__(self):
        return '%s, %s: %s' % (self.account, self.product, self.begin_day_at)

    @classmethod
    def build_user_weekly_bill(cls, account, params):
        record = cls.objects.filter(account=account, product=params['product'],
            week_in_year=params['weekInYear'], begin_day_at=params['beginAt'],
            end_day_at=params['endAt']).first()
        if record:
            record.request_count = params['requestCount']
            record.bill_count = params['billCount']
            record.total_amount = params['amount']
            record.updated_at = datetime.datetime.fromtimestamp(params['updateAt'])
            record.save()
        else:
            cls.create(account=account, product=params['product'],
                week_in_year=params['weekInYear'], begin_day_at=params['beginAt'],
                end_day_at=params['endAt'], request_count=params['requestCount'],
                bill_count=params['billCount'], total_amount=params['amount'],
                updated_at=datetime.datetime.fromtimestamp(params['updateAt']))


class BillMonthly(BaseBillModel):
    month_at = models.DateField(_('月份'))

    class Meta:
        managed = True
        db_table = 'bill_monthly'

    def __str__(self):
        return '%s, %s: %s' % (self.account, self.product, self.month_at)

    @classmethod
    def build_user_monthly_bill(cls, account, params):
        record = cls.objects.filter(account=account, product=params['product'],
            month_at=params['month']).first()
        if record:
            record.request_count = params['requestCount']
            record.bill_count = params['billCount']
            record.total_amount = params['amount']
            record.updated_at = datetime.datetime.fromtimestamp(params['updateAt'])
            record.save()
        else:
            cls.create(account=account, product=params['product'],
                month_at=params['month'], request_count=params['requestCount'],
                bill_count=params['billCount'], total_amount=params['amount'],
                updated_at=datetime.datetime.fromtimestamp(params['updateAt']))

