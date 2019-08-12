from django.db import models
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

# Create your models here.

class ContrSchedule(models.Model):

    objid = models.FloatField(blank=True, primary_key=True)
    schedule_id = models.CharField(max_length=40, blank=True, null=True)
    s_schedule_id = models.CharField(max_length=40, blank=True, null=True)
    schedule_title = models.CharField(max_length=160, blank=True, null=True)
    gross_line_pr = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    net_line_pr = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    sched_adj_amt = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    sched_tax_pct = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    sched_tax_amt = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    sched_net_amt = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    fob = models.CharField(max_length=40, blank=True, null=True)
    close_eff_dt = models.DateTimeField(blank=True, null=True)
    close_crdt_ind = models.FloatField(blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    last_xfer = models.DateTimeField(blank=True, null=True)
    start_dt = models.DateTimeField(blank=True, null=True)
    due_offset = models.FloatField(blank=True, null=True)
    frequency = models.FloatField(blank=True, null=True)
    invc_terms = models.CharField(max_length=80, blank=True, null=True)
    bill_group = models.CharField(max_length=30, blank=True, null=True)
    bill_option = models.FloatField(blank=True, null=True)
    itm_start_dt = models.DateTimeField(blank=True, null=True)
    itm_end_dt = models.DateTimeField(blank=True, null=True)
    cycle_start_dt = models.DateTimeField(blank=True, null=True)
    ship_attn = models.CharField(max_length=30, blank=True, null=True)
    s_ship_attn = models.CharField(max_length=30, blank=True, null=True)
    ship_attn2 = models.CharField(max_length=40, blank=True, null=True)
    s_ship_attn2 = models.CharField(max_length=40, blank=True, null=True)
    bill_attn = models.CharField(max_length=30, blank=True, null=True)
    s_bill_attn = models.CharField(max_length=30, blank=True, null=True)
    bill_attn2 = models.CharField(max_length=40, blank=True, null=True)
    s_bill_attn2 = models.CharField(max_length=40, blank=True, null=True)
    fsvc_end_dt = models.DateTimeField(blank=True, null=True)
    fsvc_start_dt = models.DateTimeField(blank=True, null=True)
    lsvc_end_dt = models.DateTimeField(blank=True, null=True)
    cycle_chg_ind = models.FloatField(blank=True, null=True)
    ship_via = models.CharField(max_length=80, blank=True, null=True)
    dev = models.FloatField(blank=True, null=True)
    ship_amt = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    handling_cost = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    total_grand = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    last_p_line_no = models.FloatField(blank=True, null=True)
    item_count = models.FloatField(blank=True, null=True)
    schedule2contract = models.FloatField(blank=True, null=True)
    bill_to2site = models.FloatField(blank=True, null=True)
    ship_to2site = models.FloatField(blank=True, null=True)
    default_prog2price_prog = models.FloatField(blank=True, null=True)
    bill_addr2address = models.FloatField(blank=True, null=True)
    ship_addr2address = models.FloatField(blank=True, null=True)
    x_migracion = models.FloatField(blank=True, null=True)
    contr_sc2hgbst_elm = models.FloatField(blank=True, null=True)
    contr_fob2hgbst_elm = models.FloatField(blank=True, null=True)
    contr_ship2hgbst_elm = models.FloatField(blank=True, null=True)

    class Meta:
        in_db = 'smart_gg'
        managed = False
        db_table = '\"SA\".\"TABLE_CONTR_SCHEDULE\"'

